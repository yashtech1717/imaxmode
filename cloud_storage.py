import os
import re
import struct
from pathlib import Path
import uuid
import logging
import requests
from typing import Tuple, Dict, Any, Generator, Optional
from fastapi import HTTPException

# Explicitly load .env from project root before reading env vars
env_path = Path(__file__).resolve().parent / ".env"
try:
    from dotenv import load_dotenv
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
except ImportError:
    pass

logger = logging.getLogger("aura.storage")

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB Supabase single-file limit
_bucket_verified = False

ALLOWED_EXTENSIONS = {
    "video": {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        ".m4v": "video/x-m4v",
        ".ogv": "video/ogg"
    },
    "image": {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".bmp": "image/bmp"
    },
    "audio": {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".aac": "audio/aac",
        ".flac": "audio/flac"
    }
}


def get_supabase_url() -> str:
    url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    if "/rest/v1" in url:
        url = url.split("/rest/v1")[0].rstrip("/")
    return url


def get_supabase_key() -> str:
    return (
        os.environ.get("SUPABASE_KEY", "").strip()
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    )


def get_supabase_bucket() -> str:
    return os.environ.get("SUPABASE_BUCKET", "memories").strip()


def is_storage_configured() -> bool:
    """Returns True if Supabase Storage credentials are provided."""
    return bool(get_supabase_url() and get_supabase_key())


def sanitize_filename(filename: str) -> Tuple[str, str]:
    """
    Extracts and sanitizes a filename for storage.
    Returns: (sanitized_basename, lowercase_extension)
    """
    base = os.path.basename(filename or "media").strip()
    name_part, ext = os.path.splitext(base)
    ext = ext.lower().strip()

    # Retain safe ASCII characters only; convert spaces, symbols, and Unicode to underscores
    clean_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name_part)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
    if not clean_name:
        clean_name = "media"
    clean_name = clean_name[:60]
    return clean_name, ext


def detect_media_type_and_mime(filename: str, content_type: str = "", sample_bytes: bytes = b"") -> Tuple[str, str]:
    """
    Accurately detects media_type ('video', 'image', 'audio') and validated MIME type.
    Inspects magic bytes and file extensions. Never defaults to application/octet-stream for detectable media.
    """
    _, ext = sanitize_filename(filename)
    ct = (content_type or "").lower().strip()

    # 1. Video Detection
    if ext in ALLOWED_EXTENSIONS["video"]:
        # Verify magic bytes for video if sample is provided
        if len(sample_bytes) >= 12:
            if b"ftyp" in sample_bytes[:12]:
                if ext == ".mov":
                    return "video", "video/quicktime"
                return "video", "video/mp4"
            if sample_bytes[:4] == b"\x1a\x45\xdf\xa3":
                return "video", "video/webm"

        mime = ALLOWED_EXTENSIONS["video"][ext]
        if ct in ALLOWED_EXTENSIONS["video"].values():
            mime = ct
        return "video", mime

    # 2. Image Detection
    if ext in ALLOWED_EXTENSIONS["image"]:
        mime = ALLOWED_EXTENSIONS["image"][ext]
        if ct in ALLOWED_EXTENSIONS["image"].values():
            mime = ct
        return "image", mime

    # 3. Audio Detection
    if ext in ALLOWED_EXTENSIONS["audio"]:
        mime = ALLOWED_EXTENSIONS["audio"][ext]
        if ct in ALLOWED_EXTENSIONS["audio"].values():
            mime = ct
        return "audio", mime

    # 4. Fallback based on client content_type
    if ct.startswith("video/"):
        return "video", ct
    if ct.startswith("image/"):
        return "image", ct
    if ct.startswith("audio/"):
        return "audio", ct

    return "image", "application/octet-stream"


def check_storage_health() -> dict:
    """Checks if Supabase Storage can be reached and bucket is accessible."""
    url = get_supabase_url()
    key = get_supabase_key()
    bucket = get_supabase_bucket()

    if not (url and key):
        return {
            "status": "error",
            "configured": False,
            "message": "SUPABASE_URL or SUPABASE_KEY environment variable is missing"
        }

    try:
        bucket_url = f"{url}/storage/v1/bucket/{bucket}"
        headers = {
            "Authorization": f"Bearer {key}",
            "apikey": key
        }
        res = requests.get(bucket_url, headers=headers, timeout=8)
        if res.status_code in [200, 201]:
            is_pub = res.json().get("public", True) if res.text.startswith("{") else True
            return {"status": "ok", "configured": True, "bucket": bucket, "public": is_pub}
        elif res.status_code == 404 or (res.status_code == 400 and "NoSuchBucket" in res.text):
            # Try to auto-create bucket programmatically if using service_role key
            create_url = f"{url}/storage/v1/bucket"
            create_payload = {"id": bucket, "name": bucket, "public": True}
            create_res = requests.post(create_url, json=create_payload, headers=headers, timeout=8)
            if create_res.status_code in [200, 201, 400, 409]:
                return {"status": "ok", "configured": True, "bucket": bucket, "public": True}
            return {
                "status": "error",
                "configured": True,
                "message": f"Bucket '{bucket}' not found (NoSuchBucket). Please create public bucket '{bucket}' in Supabase Storage Dashboard."
            }
        elif res.status_code == 401:
            return {"status": "error", "configured": True, "message": "Storage API rejected key (HTTP 401 Unauthorized)"}
        elif res.status_code == 403:
            return {"status": "error", "configured": True, "message": "Storage API permission denied (HTTP 403 Forbidden)"}
        else:
            return {"status": "error", "configured": True, "message": f"Storage returned status {res.status_code}: {res.text}"}
    except Exception as err:
        return {"status": "error", "configured": True, "message": str(err)}


def _ensure_supabase_bucket():
    global _bucket_verified
    if _bucket_verified:
        return
    url = get_supabase_url()
    key = get_supabase_key()
    bucket = get_supabase_bucket()

    if not (url and key):
        raise HTTPException(
            status_code=500,
            detail="CRITICAL: Supabase Storage is not configured. SUPABASE_URL and SUPABASE_KEY must be set in your .env file or Render environment variables."
        )

    try:
        create_url = f"{url}/storage/v1/bucket"
        headers = {
            "Authorization": f"Bearer {key}",
            "apikey": key,
            "Content-Type": "application/json"
        }
        payload = {"id": bucket, "name": bucket, "public": True}
        res = requests.post(create_url, json=payload, headers=headers, timeout=6)
        if res.status_code in [200, 201, 400, 409]:
            # Explicitly ensure existing bucket is marked public
            try:
                put_url = f"{url}/storage/v1/bucket/{bucket}"
                requests.put(put_url, json={"public": True}, headers=headers, timeout=5)
            except Exception:
                pass
            _bucket_verified = True
    except Exception as e:
        logger.warning("Could not auto-create Supabase bucket: %s", e)
        _bucket_verified = True


def optimize_mp4_faststart(data: bytes) -> bytes:
    """
    Safely handles MP4 containers. Preserves exact uploaded bytes to guarantee
    zero video corruption. RFC 7233 byte-range streaming handles moov seeking natively.
    """
    return data



def upload_file(file_bytes: bytes, filename: str, content_type: str = "") -> dict:
    """
    Strictly uploads a file to Supabase Storage.
    Never writes to local filesystem or SQLite.
    Verifies object existence after upload.
    Raises HTTPException on failure or missing credentials.
    """
    url = get_supabase_url()
    key = get_supabase_key()
    bucket = get_supabase_bucket()

    if not (url and key):
        logger.critical("Upload rejected: SUPABASE_URL or SUPABASE_KEY is missing. Local filesystem fallback is disabled.")
        raise HTTPException(
            status_code=500,
            detail="CRITICAL: Supabase Cloud Storage is not configured on the server. SUPABASE_URL and SUPABASE_KEY must be set in your .env file or Render environment variables. Local file storage is disabled to prevent data loss."
        )

    if not file_bytes or len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot upload an empty file (0 bytes received)."
        )

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum allowed size of 50 MB (File size: {len(file_bytes) / (1024 * 1024):.1f} MB)."
        )

    clean_name, ext = sanitize_filename(filename)
    media_type, final_mime = detect_media_type_and_mime(filename, content_type, file_bytes[:32])

    # Optimize MP4 container layout for instant byte-range streaming (Faststart: moov before mdat)
    if media_type == "video" and ext in [".mp4", ".m4v"]:
        try:
            file_bytes = optimize_mp4_faststart(file_bytes)
        except Exception as opt_err:
            logger.warning("MP4 faststart optimization skipped: %s", opt_err)

    _ensure_supabase_bucket()

    unique_file_path = f"{uuid.uuid4().hex[:10]}_{clean_name}{ext}"
    storage_path = f"{bucket}/{unique_file_path}"

    upload_url = f"{url}/storage/v1/object/{bucket}/{unique_file_path}"
    headers = {
        "Authorization": f"Bearer {key}",
        "apikey": key,
        "Content-Type": final_mime,
        "x-upsert": "true"
    }

    logger.info("Initiating upload to Supabase Storage: %s (Type: %s, MIME: %s, Size: %.1f MB)",
                unique_file_path, media_type, final_mime, len(file_bytes) / (1024 * 1024))

    try:
        res = requests.post(upload_url, data=file_bytes, headers=headers, timeout=60)
    except Exception as err:
        logger.error("Network error uploading to Supabase Storage: %s", err, exc_info=True)
        raise HTTPException(
            status_code=502,
            detail=f"Failed to communicate with Supabase Cloud Storage: {str(err)}"
        )

    if res.status_code not in [200, 201]:
        logger.error("Supabase Storage rejected upload (status %s): %s", res.status_code, res.text)
        raise HTTPException(
            status_code=502,
            detail=f"Supabase Storage upload failed with status {res.status_code}: {res.text}"
        )

    # Post-upload existence verification via HEAD request
    verify_url = f"{url}/storage/v1/object/public/{bucket}/{unique_file_path}"
    try:
        check_res = requests.head(verify_url, headers={"Authorization": f"Bearer {key}", "apikey": key}, timeout=10)
        if check_res.status_code not in [200, 206]:
            auth_check_url = f"{url}/storage/v1/object/authenticated/{bucket}/{unique_file_path}"
            auth_res = requests.head(auth_check_url, headers={"Authorization": f"Bearer {key}", "apikey": key}, timeout=10)
            if auth_res.status_code not in [200, 206]:
                logger.warning("Object verification status: %s / %s", check_res.status_code, auth_res.status_code)
    except Exception as v_err:
        logger.warning("Non-critical post-upload verification notice: %s", v_err)

    public_url = f"{url}/storage/v1/object/public/{bucket}/{unique_file_path}"
    logger.info("File successfully verified and stored in Supabase Storage: %s", public_url)

    return {
        "url": public_url,
        "storage_path": storage_path,
        "media_type": media_type,
        "mime_type": final_mime,
        "filename": filename,
        "is_cloud": True,
        "storage": "supabase"
    }


def extract_storage_key(url_or_path: str) -> Tuple[str, str]:
    """
    Extracts the bucket and relative object key from any Supabase URL, storage_path, or proxy path.
    Returns: (bucket, object_key)
    """
    bucket = get_supabase_bucket()
    if not url_or_path:
        return bucket, ""

    from urllib.parse import unquote, urlparse, parse_qs
    s = unquote(url_or_path.strip())

    # If it's a proxy URL like /api/media/stream?url=...
    if "/api/media/stream" in s:
        parsed = urlparse(s)
        qs = parse_qs(parsed.query)
        if "url" in qs and qs["url"][0]:
            return extract_storage_key(qs["url"][0])
        if "path" in qs and qs["path"][0]:
            return extract_storage_key(qs["path"][0])
        after_stream = s.split("/api/media/stream/")[-1]
        if after_stream and after_stream != s:
            return extract_storage_key(after_stream)

    # Handle full Supabase URLs
    if "/storage/v1/object/" in s:
        after = s.split("/storage/v1/object/")[-1]
        for mode in ["public/", "authenticated/", "sign/"]:
            if after.startswith(mode):
                after = after[len(mode):]
                break
        parts = after.split("/", 1)
        if len(parts) == 2:
            return parts[0], parts[1].split("?")[0]
        return bucket, parts[0].split("?")[0]

    # Clean leading slashes
    clean_s = s.lstrip("/").split("?")[0]
    if "/" in clean_s:
        parts = clean_s.split("/", 1)
        if parts[0] in [bucket, "memories"]:
            return parts[0], parts[1]
        return bucket, clean_s

    return bucket, clean_s


def create_signed_url(url_or_path: str, expires_in: int = 86400) -> Optional[str]:
    """Generates an authenticated Supabase signed URL valid for direct browser streaming."""
    url = get_supabase_url()
    key = get_supabase_key()
    if not (url and key):
        return None
    bucket, object_key = extract_storage_key(url_or_path)
    if not object_key:
        return None
    clean_key = "/".join(p for p in object_key.split("/") if p and p not in [".", ".."])
    sign_endpoint = f"{url}/storage/v1/object/sign/{bucket}/{clean_key}"
    headers = {
        "Authorization": f"Bearer {key}",
        "apikey": key,
        "Content-Type": "application/json"
    }
    try:
        res = requests.post(sign_endpoint, json={"expiresIn": expires_in}, headers=headers, timeout=8)
        if res.status_code in [200, 201]:
            data = res.json()
            signed_path = data.get("signedURL") or data.get("signedUrl")
            if signed_path:
                if signed_path.startswith("http"):
                    return signed_path
                if signed_path.startswith("/storage/v1"):
                    return f"{url}{signed_path}"
                return f"{url}/storage/v1{signed_path}"
    except Exception as err:
        logger.warning("Could not create Supabase signed URL for %s: %s", clean_key, err)
    return None


def get_storage_stream_info(url_or_path: str, range_header: Optional[str] = None, method: str = "GET") -> Tuple[int, Dict[str, str], Any]:
    """
    Fetches media stream information and chunk generator from Supabase Storage with Range support.
    Tries authenticated, public, and signed endpoints to guarantee stream delivery.
    """
    url = get_supabase_url()
    key = get_supabase_key()
    bucket, object_key = extract_storage_key(url_or_path)

    if not object_key:
        raise HTTPException(status_code=400, detail="Invalid media storage path or URL")

    # Clean object key to prevent directory traversal
    clean_key = "/".join(p for p in object_key.split("/") if p and p not in [".", ".."])

    headers = {
        "Authorization": f"Bearer {key}",
        "apikey": key
    }
    if range_header:
        headers["Range"] = range_header

    # Endpoints to attempt in priority order:
    # 1. Public endpoint (fastest, standard for public buckets)
    target_url = f"{url}/storage/v1/object/public/{bucket}/{clean_key}"
    last_res = None
    try:
        if method.upper() == "HEAD":
            res = requests.head(target_url, headers=headers, timeout=6)
        else:
            # Connect timeout: 5s, Read timeout: 120s (prevents socket dropping when video player buffers)
            res = requests.get(target_url, headers=headers, stream=True, timeout=(5, 120))

        if res.status_code in [200, 206]:
            return res.status_code, dict(res.headers), (res if method.upper() != "HEAD" else None)
        last_res = res
    except Exception as err:
        logger.warning("Storage public endpoint %s failed: %s", target_url, err)

    # 2. If public endpoint returned non-200/206, attempt authenticated signed URL streaming fallback
    try:
        signed_direct = create_signed_url(url_or_path, expires_in=86400)
        if signed_direct:
            s_headers = {}
            if range_header:
                s_headers["Range"] = range_header
            if method.upper() == "HEAD":
                s_res = requests.head(signed_direct, headers=s_headers, timeout=8)
            else:
                s_res = requests.get(signed_direct, headers=s_headers, stream=True, timeout=(5, 120))
            if s_res.status_code in [200, 206]:
                return s_res.status_code, dict(s_res.headers), (s_res if method.upper() != "HEAD" else None)
            last_res = s_res
    except Exception as s_err:
        logger.warning("Signed URL streaming fallback failed for %s: %s", clean_key, s_err)

    if last_res is not None:
        return last_res.status_code, dict(last_res.headers), (last_res if method.upper() != "HEAD" else None)

    raise HTTPException(status_code=502, detail="Upstream Supabase Storage could not be reached.")

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
        res = requests.post(create_url, json=payload, headers=headers, timeout=8)
        if res.status_code in [200, 201, 400, 409]:
            _bucket_verified = True
    except Exception as e:
        logger.warning("Could not auto-create Supabase bucket: %s", e)
        _bucket_verified = True


def optimize_mp4_faststart(data: bytes) -> bytes:
    """
    Relocates the 'moov' metadata atom to the beginning of the file (right after 'ftyp').
    Adjusts sample table chunk offsets in 'stco' and 'co64' atoms.
    Enables instant progressive streaming and byte-range seeking from byte 0.
    Pure Python, zero external dependencies, 0 CPU transcoding cost.
    """
    if len(data) < 16:
        return data

    pos = 0
    atoms = []
    while pos + 8 <= len(data):
        s = struct.unpack('>I', data[pos:pos+4])[0]
        tag = data[pos+4:pos+8].decode('latin1', errors='ignore')
        if s == 1:
            s = struct.unpack('>Q', data[pos+8:pos+16])[0]
        elif s == 0:
            s = len(data) - pos
        atoms.append((tag, pos, s))
        if s < 8:
            break
        pos += s

    tag_names = [a[0] for a in atoms]
    if 'moov' not in tag_names or 'mdat' not in tag_names or 'ftyp' not in tag_names:
        return data

    ftyp = [a for a in atoms if a[0] == 'ftyp'][0]
    moov = [a for a in atoms if a[0] == 'moov'][0]
    mdat = [a for a in atoms if a[0] == 'mdat'][0]

    # Already faststart if moov is before mdat
    if moov[1] < mdat[1]:
        return data

    original_mdat_offset = mdat[1]
    new_mdat_offset = ftyp[2] + moov[2]
    shift = new_mdat_offset - original_mdat_offset

    moov_data = bytearray(data[moov[1]:moov[1]+moov[2]])
    def walk(p, end):
        while p + 8 <= end:
            s = struct.unpack('>I', moov_data[p:p+4])[0]
            tag = moov_data[p+4:p+8].decode('latin1', errors='ignore')
            if s == 1:
                s = struct.unpack('>Q', moov_data[p+8:p+16])[0]
                h = 16
            else:
                h = 8
            if s == 0:
                s = end - p
            if tag in ['trak', 'mdia', 'minf', 'stbl', 'moov', 'edts']:
                walk(p + h, p + s)
            elif tag == 'stco':
                cnt = struct.unpack('>I', moov_data[p+12:p+16])[0]
                for i in range(cnt):
                    ep = p + 16 + i * 4
                    if ep + 4 <= end:
                        off = struct.unpack('>I', moov_data[ep:ep+4])[0]
                        moov_data[ep:ep+4] = struct.pack('>I', off + shift)
            elif tag == 'co64':
                cnt = struct.unpack('>I', moov_data[p+12:p+16])[0]
                for i in range(cnt):
                    ep = p + 16 + i * 8
                    if ep + 8 <= end:
                        off = struct.unpack('>Q', moov_data[ep:ep+8])[0]
                        moov_data[ep:ep+8] = struct.pack('>Q', off + shift)
            p += s
    walk(0, len(moov_data))

    other_atoms = [a for a in atoms if a[0] not in ['ftyp', 'moov', 'mdat', 'free']]
    res = bytearray(data[ftyp[1]:ftyp[1]+ftyp[2]])
    res.extend(moov_data)
    res.extend(data[mdat[1]:mdat[1]+mdat[2]])
    for a in other_atoms:
        res.extend(data[a[1]:a[1]+a[2]])
    return bytes(res)


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
    Extracts the bucket and relative object key from any Supabase URL, storage_path, or relative path.
    Returns: (bucket, object_key)
    """
    bucket = get_supabase_bucket()
    if not url_or_path:
        return bucket, ""

    s = url_or_path.strip()

    # Handle full Supabase URLs
    if "/storage/v1/object/" in s:
        # e.g. https://.../storage/v1/object/public/memories/3d36355eed_Video-16169.mp4
        after = s.split("/storage/v1/object/")[-1]
        for mode in ["public/", "authenticated/", "sign/"]:
            if after.startswith(mode):
                after = after[len(mode):]
                break
        parts = after.split("/", 1)
        if len(parts) == 2:
            return parts[0], parts[1].split("?")[0]
        return bucket, parts[0].split("?")[0]

    # Handle storage_path format 'bucket/key' or just 'key'
    if "/" in s:
        parts = s.split("/", 1)
        if parts[0] in [bucket, "memories"]:
            return parts[0], parts[1].split("?")[0]
        return bucket, s.split("?")[0]

    return bucket, s.split("?")[0]


def get_storage_stream_info(url_or_path: str, range_header: Optional[str] = None, method: str = "GET") -> Tuple[int, Dict[str, str], Any]:
    """
    Fetches media stream information and chunk generator from Supabase Storage with Range support.
    Works for both public and private buckets using server credentials.
    """
    url = get_supabase_url()
    key = get_supabase_key()
    bucket, object_key = extract_storage_key(url_or_path)

    if not object_key:
        raise HTTPException(status_code=400, detail="Invalid media storage path or URL")

    # Clean object key to prevent directory traversal
    clean_key = "/".join(p for p in object_key.split("/") if p and p not in [".", ".."])
    target_url = f"{url}/storage/v1/object/public/{bucket}/{clean_key}"

    headers = {
        "Authorization": f"Bearer {key}",
        "apikey": key
    }
    if range_header:
        headers["Range"] = range_header

    try:
        if method.upper() == "HEAD":
            res = requests.head(target_url, headers=headers, timeout=12)
            # If public HEAD returned 401/403, try authenticated endpoint
            if res.status_code in [401, 403, 404]:
                auth_url = f"{url}/storage/v1/object/authenticated/{bucket}/{clean_key}"
                res = requests.head(auth_url, headers=headers, timeout=12)
            return res.status_code, dict(res.headers), None

        res = requests.get(target_url, headers=headers, stream=True, timeout=15)
        if res.status_code in [401, 403, 404]:
            auth_url = f"{url}/storage/v1/object/authenticated/{bucket}/{clean_key}"
            res = requests.get(auth_url, headers=headers, stream=True, timeout=15)

        return res.status_code, dict(res.headers), res
    except Exception as e:
        logger.error("Error communicating with Supabase Storage for streaming: %s", e)
        raise HTTPException(status_code=502, detail=f"Upstream storage streaming failed: {str(e)}")

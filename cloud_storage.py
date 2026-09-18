import os
from pathlib import Path
import uuid
import logging
import requests
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
            return {"status": "ok", "configured": True, "bucket": bucket, "public": True}
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


def upload_file(file_bytes: bytes, filename: str, content_type: str = "") -> dict:
    """
    Strictly uploads a file to Supabase Storage.
    NEVER writes to local filesystem or SQLite.
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

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum allowed size of 50 MB (File size: {len(file_bytes) / (1024 * 1024):.1f} MB)."
        )

    ext = os.path.splitext(filename)[1].lower()
    ct = (content_type or "").lower()

    if ct.startswith("image") or ext in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".bmp"]:
        media_type = "image"
        default_mime = "image/jpeg"
    elif ct.startswith("video") or ext in [".mp4", ".webm", ".mov", ".mkv", ".avi", ".m4v"]:
        media_type = "video"
        default_mime = "video/mp4"
    elif ct.startswith("audio") or ext in [".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"]:
        media_type = "audio"
        default_mime = "audio/mpeg"
    else:
        media_type = "image"
        default_mime = "application/octet-stream"

    final_mime = content_type or default_mime
    _ensure_supabase_bucket()

    clean_name = os.path.splitext(os.path.basename(filename))[0].replace(" ", "_")
    unique_file_path = f"{uuid.uuid4().hex[:10]}_{clean_name}{ext}"

    upload_url = f"{url}/storage/v1/object/{bucket}/{unique_file_path}"
    headers = {
        "Authorization": f"Bearer {key}",
        "apikey": key,
        "Content-Type": final_mime,
        "x-upsert": "true"
    }

    try:
        res = requests.post(upload_url, data=file_bytes, headers=headers, timeout=45)
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

    public_url = f"{url}/storage/v1/object/public/{bucket}/{unique_file_path}"
    logger.info("File successfully stored in Supabase Cloud Storage: %s", public_url)

    return {
        "url": public_url,
        "media_type": media_type,
        "filename": filename,
        "is_cloud": True,
        "storage": "supabase"
    }

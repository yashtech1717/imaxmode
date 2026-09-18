import os
import uuid
import logging
import requests
from fastapi import HTTPException

logger = logging.getLogger("aura.storage")

# Supabase Storage Configuration (Strict Cloud Only - No Local Fallback)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
if "/rest/v1" in SUPABASE_URL:
    SUPABASE_URL = SUPABASE_URL.split("/rest/v1")[0].rstrip("/")

SUPABASE_KEY = (
    os.environ.get("SUPABASE_KEY", "").strip() 
    or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
)
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "memories").strip()
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB Supabase single-file limit

_bucket_verified = False


def is_storage_configured() -> bool:
    """Returns True if Supabase Storage credentials are provided."""
    return bool(SUPABASE_URL and SUPABASE_KEY)


def check_storage_health() -> dict:
    """Checks if Supabase Storage can be reached and bucket is accessible."""
    if not is_storage_configured():
        return {
            "status": "error",
            "configured": False,
            "message": "SUPABASE_URL or SUPABASE_KEY environment variable is missing"
        }

    try:
        url = f"{SUPABASE_URL}/storage/v1/bucket/{SUPABASE_BUCKET}"
        headers = {
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "apikey": SUPABASE_KEY
        }
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code in [200, 201]:
            return {"status": "ok", "configured": True, "bucket": SUPABASE_BUCKET, "public": True}
        elif res.status_code == 404:
            # Try to auto-create bucket
            create_url = f"{SUPABASE_URL}/storage/v1/bucket"
            create_payload = {"id": SUPABASE_BUCKET, "name": SUPABASE_BUCKET, "public": True}
            create_res = requests.post(create_url, json=create_payload, headers=headers, timeout=6)
            if create_res.status_code in [200, 201, 400, 409]:
                return {"status": "ok", "configured": True, "bucket": SUPABASE_BUCKET, "public": True}
            return {"status": "error", "configured": True, "message": f"Bucket '{SUPABASE_BUCKET}' not found and auto-create returned {create_res.status_code}"}
        else:
            return {"status": "error", "configured": True, "message": f"Storage returned status {res.status_code}: {res.text}"}
    except Exception as err:
        return {"status": "error", "configured": True, "message": str(err)}


def _ensure_supabase_bucket():
    global _bucket_verified
    if _bucket_verified:
        return
    if not is_storage_configured():
        raise HTTPException(
            status_code=500,
            detail="Supabase Storage is not configured. SUPABASE_URL and SUPABASE_KEY must be set in environment variables."
        )

    try:
        url = f"{SUPABASE_URL}/storage/v1/bucket"
        headers = {
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "id": SUPABASE_BUCKET,
            "name": SUPABASE_BUCKET,
            "public": True
        }
        res = requests.post(url, json=payload, headers=headers, timeout=6)
        if res.status_code in [200, 201, 400, 409]:
            _bucket_verified = True
            logger.info(f"Supabase Storage bucket '{SUPABASE_BUCKET}' ready.")
    except Exception as e:
        logger.warning(f"Could not auto-create Supabase bucket: {e}")
        _bucket_verified = True


def upload_file(file_bytes: bytes, filename: str, content_type: str = "") -> dict:
    """
    Strictly uploads a file to Supabase Storage.
    NEVER writes to local filesystem or SQLite.
    Raises HTTPException on failure or missing credentials.
    """
    if not is_storage_configured():
        logger.critical("Upload rejected: SUPABASE_URL or SUPABASE_KEY is missing. Local filesystem fallback is disabled.")
        raise HTTPException(
            status_code=500,
            detail="CRITICAL: Supabase Cloud Storage is not configured on the server. SUPABASE_URL and SUPABASE_KEY must be set in Render environment variables. Local file storage is disabled to prevent data loss."
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

    upload_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{unique_file_path}"
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "apikey": SUPABASE_KEY,
        "Content-Type": final_mime,
        "x-upsert": "true"
    }

    try:
        res = requests.post(upload_url, data=file_bytes, headers=headers, timeout=45)
    except Exception as err:
        logger.error(f"Network error uploading to Supabase Storage: {err}", exc_info=True)
        raise HTTPException(
            status_code=502,
            detail=f"Failed to communicate with Supabase Cloud Storage: {str(err)}"
        )

    if res.status_code not in [200, 201]:
        logger.error(f"Supabase Storage rejected upload (status {res.status_code}): {res.text}")
        raise HTTPException(
            status_code=502,
            detail=f"Supabase Storage upload failed with status {res.status_code}: {res.text}"
        )

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{unique_file_path}"
    logger.info(f"File successfully stored in Supabase Cloud Storage: {public_url}")

    return {
        "url": public_url,
        "media_type": media_type,
        "filename": filename,
        "is_cloud": True,
        "storage": "supabase"
    }

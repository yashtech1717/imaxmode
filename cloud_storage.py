import os
import uuid
import logging
import requests

logger = logging.getLogger("aura.storage")

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Supabase Storage Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip() or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "memories").strip()

has_supabase = bool(SUPABASE_URL and SUPABASE_KEY)
_bucket_initialized = False

def _ensure_supabase_bucket():
    global _bucket_initialized
    if not has_supabase or _bucket_initialized:
        return
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
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        if res.status_code in [200, 201, 400, 409]:
            _bucket_initialized = True
            logger.info(f"Supabase bucket '{SUPABASE_BUCKET}' verified.")
    except Exception as e:
        logger.warning(f"Could not auto-verify Supabase bucket: {e}")
        _bucket_initialized = True


def upload_file(file_bytes: bytes, filename: str, content_type: str = "") -> dict:
    """
    Uploads a file to Supabase Storage if configured; otherwise falls back to local static/uploads/.
    Returns a dict with:
        url: Permanent HTTPS public URL (Supabase) or relative path (/static/uploads/...)
        media_type: 'image' | 'video' | 'audio'
        filename: original filename
        is_cloud: bool
    """
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

    # 1. Try Supabase Storage if configured
    if has_supabase:
        try:
            _ensure_supabase_bucket()
            clean_name = os.path.splitext(os.path.basename(filename))[0].replace(" ", "_")
            file_path = f"{uuid.uuid4().hex[:8]}_{clean_name}{ext}"

            upload_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{file_path}"
            headers = {
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "apikey": SUPABASE_KEY,
                "Content-Type": final_mime,
                "x-upsert": "true"
            }

            res = requests.post(upload_url, data=file_bytes, headers=headers, timeout=30)
            if res.status_code in [200, 201]:
                public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_path}"
                logger.info(f"Uploaded to Supabase Storage: {public_url}")
                return {
                    "url": public_url,
                    "media_type": media_type,
                    "filename": filename,
                    "is_cloud": True
                }
            else:
                logger.warning(f"Supabase upload returned status {res.status_code}: {res.text}. Falling back to local.")
        except Exception as err:
            logger.error(f"Supabase upload failed ({err}). Falling back to local disk.", exc_info=True)

    # 2. Local disk fallback
    safe_name = f"{uuid.uuid4().hex[:10]}_{filename.replace(' ', '_')}"
    save_path = os.path.join(UPLOADS_DIR, safe_name)
    with open(save_path, "wb") as f:
        f.write(file_bytes)

    return {
        "url": f"/static/uploads/{safe_name}",
        "media_type": media_type,
        "filename": filename,
        "is_cloud": False
    }


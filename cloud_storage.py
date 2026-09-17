import os
import uuid
import logging

logger = logging.getLogger("aura.storage")

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Cloudinary Setup
CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL", "").strip()

has_cloudinary = False
if CLOUDINARY_URL:
    try:
        import cloudinary
        import cloudinary.uploader
        cloudinary.config(cloudinary_url=CLOUDINARY_URL)
        has_cloudinary = True
        logger.info("Cloudinary cloud media storage initialized successfully.")
    except Exception as e:
        logger.warning(f"Failed to initialize Cloudinary with CLOUDINARY_URL: {e}")
        has_cloudinary = False


def upload_file(file_bytes: bytes, filename: str, content_type: str = "") -> dict:
    """
    Uploads a file to Cloudinary if configured; otherwise saves to local static/uploads/.
    Returns a dict with:
        url: Permanent HTTPS URL (Cloudinary) or relative path (/static/uploads/...)
        media_type: 'image' | 'video' | 'audio'
        filename: original filename
        is_cloud: bool
    """
    ext = os.path.splitext(filename)[1].lower()
    ct = (content_type or "").lower()

    if ct.startswith("image") or ext in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".bmp"]:
        media_type = "image"
        cloudinary_resource_type = "image"
    elif ct.startswith("video") or ext in [".mp4", ".webm", ".mov", ".mkv", ".avi", ".m4v"]:
        media_type = "video"
        cloudinary_resource_type = "video"
    elif ct.startswith("audio") or ext in [".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"]:
        media_type = "audio"
        # In Cloudinary, audio files are handled under 'video' resource_type for streaming & waveforms
        cloudinary_resource_type = "video"
    else:
        media_type = "image"
        cloudinary_resource_type = "auto"

    # 1. Try Cloudinary if configured
    if has_cloudinary:
        try:
            import cloudinary.uploader
            clean_name = os.path.splitext(os.path.basename(filename))[0].replace(" ", "_")
            public_id = f"aura_memories/{uuid.uuid4().hex[:8]}_{clean_name}"
            
            result = cloudinary.uploader.upload(
                file_bytes,
                public_id=public_id,
                resource_type=cloudinary_resource_type,
                overwrite=True
            )
            secure_url = result.get("secure_url") or result.get("url")
            logger.info(f"Uploaded to Cloudinary: {secure_url}")
            return {
                "url": secure_url,
                "media_type": media_type,
                "filename": filename,
                "is_cloud": True
            }
        except Exception as err:
            logger.error(f"Cloudinary upload failed ({err}). Falling back to local disk.", exc_info=True)

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

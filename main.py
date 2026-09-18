import os
import logging
import uuid
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from cloud_storage import upload_file, check_storage_health, is_storage_configured
from db import (
    init_db,
    check_db_health,
    is_db_configured,
    get_site_config,
    update_site_config,
    get_chapters,
    get_chapter,
    update_chapter,
    add_new_chapter,
    delete_chapter,
    add_reply,
    get_replies,
    get_all_texts,
    add_text,
    delete_text
)

logger = logging.getLogger("aura.server")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

app = FastAPI(
    title="AURA Cinematic 2-Role Birthday Canvas",
    description="Dynamic cinematic birthday portal with Yash Admin CMS, Glory Viewer experience, and interactive media player",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- Pydantic Schemas ---
class LoginRequest(BaseModel):
    username: str
    password: str

class ConfigUpdate(BaseModel):
    headline_word1: Optional[str] = None
    headline_word2: Optional[str] = None
    giant_word: Optional[str] = None
    top_badge: Optional[str] = None
    typing_text: Optional[str] = None
    spec_pill1: Optional[str] = None
    spec_pill2: Optional[str] = None

class ChapterUpdate(BaseModel):
    step_index: int
    theme: Optional[str] = None
    badge: Optional[str] = None
    counter: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None
    media_name: Optional[str] = None

class ReplyCreate(BaseModel):
    sender: Optional[str] = "Glory"
    message: str = Field(..., min_length=1, max_length=3000)
    chapter_index: Optional[int] = None
    chapter_title: Optional[str] = None

class TextCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    tag: Optional[str] = Field(default="Inspire", max_length=50)
    style_preset: Optional[str] = Field(default="minimal")
    font_size: Optional[int] = Field(default=36, ge=16, le=96)
    alignment: Optional[str] = Field(default="center")
    glow: Optional[int] = Field(default=1)

@app.on_event("startup")
def on_startup():
    logger.info("Initializing AURA Cloud Backend with Supabase...")
    db_status = check_db_health()
    storage_status = check_storage_health()

    if db_status.get("status") != "ok":
        msg = f"[FATAL] Supabase PostgreSQL check failed: {db_status.get('message')}"
        logger.critical(msg)
        if os.environ.get("TEST_MODE") != "1":
            raise RuntimeError(
                f"{msg}. Supabase PostgreSQL is required. "
                "Local SQLite fallback has been completely removed to prevent data loss."
            )
    else:
        logger.info(f"[SUPABASE DATABASE: CONNECTED] Host: {db_status.get('host')}")
        try:
            init_db()
        except Exception as err:
            logger.critical(f"Failed to run init_db: {err}")
            if os.environ.get("TEST_MODE") != "1":
                raise

    if storage_status.get("status") != "ok":
        logger.warning(f"[SUPABASE STORAGE CHECK WARNING] {storage_status.get('message')}")
    else:
        logger.info(f"[SUPABASE STORAGE: CONNECTED] Bucket: '{storage_status.get('bucket')}'")

    if db_status.get("status") == "ok" and storage_status.get("status") == "ok":
        logger.info("================================================================")
        logger.info("[SUPABASE CONFIGURATION: OK]")
        logger.info("  Database: Supabase PostgreSQL (Strict Cloud)")
        logger.info("  Storage:  Supabase Storage Bucket '%s' (Strict Cloud)", storage_status.get('bucket'))
        logger.info("  Fallback: Local SQLite & Local Filesystem are PERMANENTLY DISABLED")
        logger.info("================================================================")

# --- Root HTML Page ---
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# --- Authentication Endpoint ---
@app.post("/api/login")
def login(payload: LoginRequest):
    user = payload.username.strip()
    pwd = payload.password.strip()

    # Admin Login (Yash)
    if user.lower() == "yash" and pwd == "yashadmin17":
        return {
            "status": "success",
            "role": "admin",
            "username": "yash",
            "displayName": "YASH (ADMIN)"
        }

    # Viewer Login (Glory / glory and lory / Lory)
    if user.lower() == "glory" and pwd.lower() == "lory":
        return {
            "status": "success",
            "role": "viewer",
            "username": "Glory",
            "displayName": "GLORY"
        }

    raise HTTPException(status_code=401, detail="Invalid credentials. Please check your username and password.")

# --- Content Delivery (Both Admin & Viewer) ---
@app.get("/api/content")
def fetch_content():
    return {
        "status": "success",
        "config": get_site_config(),
        "chapters": get_chapters()
    }

# --- Admin CMS Endpoints ---
@app.post("/api/admin/config")
def set_site_config(payload: ConfigUpdate):
    dump_func = getattr(payload, "model_dump", None) or payload.dict
    updates = dump_func(exclude_unset=True)
    updated = update_site_config(updates)
    return {"status": "success", "data": updated}

@app.post("/api/admin/chapter")
def set_chapter(payload: ChapterUpdate):
    dump_func = getattr(payload, "model_dump", None) or payload.dict
    data = dump_func(exclude_unset=True)
    step_idx = data.pop("step_index")
    updated = update_chapter(step_idx, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"status": "success", "data": updated}

@app.post("/api/admin/chapter/add")
def add_chapter_endpoint():
    chapters = add_new_chapter()
    return {"status": "success", "chapters": chapters}

@app.delete("/api/admin/chapter/{step_index}")
def delete_chapter_endpoint(step_index: int):
    chapters = delete_chapter(step_index)
    return {"status": "success", "chapters": chapters}

@app.post("/api/admin/upload")
async def upload_media_file(file: UploadFile = File(...)):
    filename = file.filename or "media"
    content_type = file.content_type or ""
    contents = await file.read()

    result = upload_file(
        file_bytes=contents,
        filename=filename,
        content_type=content_type
    )

    return {
        "status": "success",
        "url": result["url"],
        "media_type": result["media_type"],
        "filename": result["filename"],
        "is_cloud": result.get("is_cloud", False)
    }

@app.get("/api/admin/replies")
def fetch_replies():
    return {"status": "success", "data": get_replies()}

# --- Viewer Reply Endpoint ---
@app.post("/api/viewer/reply")
def submit_reply(payload: ReplyCreate):
    created = add_reply(
        sender=payload.sender or "Glory",
        message=payload.message,
        chapter_index=payload.chapter_index,
        chapter_title=payload.chapter_title
    )
    return {"status": "success", "data": created}

# --- Legacy Endpoints ---
@app.get("/api/texts")
def list_texts():
    return {"status": "success", "data": get_all_texts()}

@app.post("/api/texts")
def create_text(payload: TextCreate):
    created = add_text(
        content=payload.content,
        tag=payload.tag or "Inspire",
        style_preset=payload.style_preset or "minimal",
        font_size=payload.font_size or 36,
        alignment=payload.alignment or "center",
        glow=1 if payload.glow else 0
    )
    return {"status": "success", "data": created}

@app.delete("/api/texts/{text_id}")
def remove_text(text_id: int):
    success = delete_text(text_id)
    if not success:
        raise HTTPException(status_code=404, detail="Text item not found")
    return {"status": "success", "message": f"Text {text_id} deleted successfully"}

@app.get("/health")
@app.get("/api/health")
def health_check():
    db_info = check_db_health()
    storage_info = check_storage_health()
    is_healthy = (db_info.get("status") == "ok" and storage_info.get("status") == "ok")

    return {
        "status": "healthy" if is_healthy else "degraded",
        "service": "AURA Cinematic Portal",
        "version": "2.0.0",
        "storage_mode": "supabase",
        "database": db_info,
        "storage": storage_info
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)



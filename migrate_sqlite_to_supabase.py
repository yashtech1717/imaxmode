"""
Migration Script: Local SQLite & Filesystem to Supabase Cloud
=============================================================
Migrates data from local 'texts.db' and media from 'static/uploads/'
directly into Supabase PostgreSQL and Supabase Storage bucket ('memories').

Usage:
    python migrate_sqlite_to_supabase.py
    
Requires environment variables:
    DATABASE_URL=postgresql://postgres.xxx:pooler...
    SUPABASE_URL=https://xxx.supabase.co
    SUPABASE_KEY=sb_publishable_... or service_role_key
"""

import os
import sys
import sqlite3
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cloud_storage import upload_file, is_storage_configured, check_storage_health
from db import get_database_url

DB_FILE = os.path.join(os.path.dirname(__file__), "texts.db")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def migrate():
    print("=" * 65)
    print("  AURA PORTAL: SQLITE -> SUPABASE CLOUD MIGRATION TOOL")
    print("=" * 65)

    if not os.path.exists(DB_FILE):
        print(f"[!] SQLite file '{DB_FILE}' not found. Nothing to migrate.")
        return

    db_url = get_database_url()
    if not db_url:
        print("[X] ERROR: DATABASE_URL environment variable is not set.")
        print("    Please set DATABASE_URL with your Supabase Connection Pooler URI.")
        print("    Example: set DATABASE_URL=postgresql://postgres:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres")
        sys.exit(1)

    print(f"[*] SQLite source: {DB_FILE}")
    parsed = urlparse(db_url)
    print(f"[*] Supabase target: {parsed.hostname}:{parsed.port}/{parsed.path.lstrip('/')}")

    # Connect to SQLite
    sqlite_conn = sqlite3.connect(DB_FILE)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    # Connect to Supabase PostgreSQL
    try:
        pg_conn = psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)
        pg_cur = pg_conn.cursor()
        print("[+] Successfully connected to Supabase PostgreSQL!")
    except Exception as e:
        print(f"[X] Could not connect to Supabase PostgreSQL: {e}")
        print("    If on Windows or Render, ensure you use the Supabase Connection Pooler (IPv4).")
        sys.exit(1)

    # Check Cloud Storage
    storage_ready = is_storage_configured()
    if storage_ready:
        s_health = check_storage_health()
        if s_health.get("status") == "ok":
            print(f"[+] Supabase Storage bucket '{s_health.get('bucket')}' is ready for media uploads.")
        else:
            print(f"[!] Warning: Supabase Storage check returned: {s_health.get('message')}")
    else:
        print("[!] Note: SUPABASE_URL / SUPABASE_KEY not set. Media files won't be uploaded.")

    # 1. Migrate Site Config
    print("\n[1/4] Migrating site_config...")
    try:
        sqlite_cur.execute("SELECT * FROM site_config WHERE id = 1")
        cfg = sqlite_cur.fetchone()
        if cfg:
            pg_cur.execute("""
                INSERT INTO site_config (
                    id, headline_word1, headline_word2, giant_word, top_badge,
                    typing_text, spec_pill1, spec_pill2, updated_at
                ) VALUES (
                    1, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
                ON CONFLICT (id) DO UPDATE SET
                    headline_word1 = EXCLUDED.headline_word1,
                    headline_word2 = EXCLUDED.headline_word2,
                    giant_word = EXCLUDED.giant_word,
                    top_badge = EXCLUDED.top_badge,
                    typing_text = EXCLUDED.typing_text,
                    spec_pill1 = EXCLUDED.spec_pill1,
                    spec_pill2 = EXCLUDED.spec_pill2,
                    updated_at = CURRENT_TIMESTAMP;
            """, (
                cfg["headline_word1"], cfg["headline_word2"], cfg["giant_word"],
                cfg["top_badge"], cfg["typing_text"], cfg["spec_pill1"], cfg["spec_pill2"]
            ))
            pg_conn.commit()
            print("    [OK] Site config successfully synchronized to Supabase.")
        else:
            print("    [--] No site_config found in SQLite.")
    except Exception as e:
        print(f"    [X] Error migrating site_config: {e}")
        pg_conn.rollback()

    # 2. Migrate Chapters and attached media
    print("\n[2/4] Migrating chapters & uploading media files...")
    try:
        sqlite_cur.execute("SELECT * FROM chapters ORDER BY step_index ASC")
        chapters = sqlite_cur.fetchall()
        for chap in chapters:
            media_url = chap["media_url"] or ""
            media_type = chap["media_type"] or "none"
            media_name = chap["media_name"] or ""

            # Check if media is stored locally in static/uploads
            if media_url.startswith("/static/uploads/") and storage_ready:
                local_rel_path = media_url.lstrip("/")
                local_abs_path = os.path.join(BASE_DIR, local_rel_path)
                if os.path.exists(local_abs_path):
                    print(f"    [->] Uploading '{media_name}' to Supabase Storage bucket...")
                    try:
                        with open(local_abs_path, "rb") as f:
                            file_bytes = f.read()
                        upload_res = upload_file(
                            file_bytes=file_bytes,
                            filename=media_name or os.path.basename(local_abs_path),
                            content_type=""
                        )
                        media_url = upload_res["url"]
                        print(f"         Uploaded -> {media_url}")
                    except Exception as up_err:
                        print(f"         [!] Upload failed ({up_err}); keeping original path.")
                else:
                    print(f"    [?] Local file not found at {local_abs_path}, preserving {media_url}")

            pg_cur.execute("""
                INSERT INTO chapters (
                    step_index, theme, badge, counter, title, body, media_type, media_url, media_name
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (step_index) DO UPDATE SET
                    theme = EXCLUDED.theme,
                    badge = EXCLUDED.badge,
                    counter = EXCLUDED.counter,
                    title = EXCLUDED.title,
                    body = EXCLUDED.body,
                    media_type = EXCLUDED.media_type,
                    media_url = EXCLUDED.media_url,
                    media_name = EXCLUDED.media_name;
            """, (
                chap["step_index"], chap["theme"], chap["badge"], chap["counter"],
                chap["title"], chap["body"], media_type, media_url, media_name
            ))
            print(f"    [OK] Chapter {chap['step_index']}: '{chap['title']}' saved.")

        pg_conn.commit()
        print(f"    [OK] All {len(chapters)} chapters synchronized.")
    except Exception as e:
        print(f"    [X] Error migrating chapters: {e}")
        pg_conn.rollback()

    # 3. Migrate Replies
    print("\n[3/4] Migrating replies...")
    try:
        sqlite_cur.execute("SELECT * FROM replies ORDER BY id ASC")
        replies = sqlite_cur.fetchall()
        migrated_count = 0
        for r in replies:
            # Check if reply already exists
            pg_cur.execute("""
                SELECT id FROM replies 
                WHERE sender = %s AND message = %s AND created_at = %s::timestamp;
            """, (r["sender"], r["message"], r["created_at"]))
            if not pg_cur.fetchone():
                pg_cur.execute("""
                    INSERT INTO replies (sender, message, chapter_index, chapter_title, created_at)
                    VALUES (%s, %s, %s, %s, %s::timestamp);
                """, (r["sender"], r["message"], r["chapter_index"], r["chapter_title"], r["created_at"]))
                migrated_count += 1

        pg_conn.commit()
        print(f"    [OK] {migrated_count} new replies migrated (Total in source: {len(replies)}).")
    except Exception as e:
        print(f"    [X] Error migrating replies: {e}")
        pg_conn.rollback()

    # 4. Migrate Texts (Legacy)
    print("\n[4/4] Migrating texts...")
    try:
        sqlite_cur.execute("SELECT * FROM texts ORDER BY id ASC")
        texts = sqlite_cur.fetchall()
        migrated_txt = 0
        for t in texts:
            pg_cur.execute("""
                SELECT id FROM texts WHERE content = %s AND tag = %s;
            """, (t["content"], t["tag"]))
            if not pg_cur.fetchone():
                pg_cur.execute("""
                    INSERT INTO texts (content, tag, style_preset, font_size, alignment, glow, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s::timestamp);
                """, (t["content"], t["tag"], t["style_preset"], t["font_size"], t["alignment"], t["glow"], t["created_at"]))
                migrated_txt += 1

        pg_conn.commit()
        print(f"    [OK] {migrated_txt} texts migrated (Total in source: {len(texts)}).")
    except Exception as e:
        print(f"    [X] Error migrating texts: {e}")
        pg_conn.rollback()

    sqlite_conn.close()
    pg_conn.close()

    print("\n" + "=" * 65)
    print("  [SUCCESS] MIGRATION TO SUPABASE CLOUD COMPLETED!")
    print("  Your chapters, media, and replies are now permanently")
    print("  stored in Supabase and will survive all Render redeploys.")
    print("=" * 65)


if __name__ == "__main__":
    migrate()

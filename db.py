import os
import logging
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger("aura.db")


def get_database_url() -> str:
    """Retrieves and normalizes the Supabase PostgreSQL connection URL."""
    url = os.environ.get("DATABASE_URL", "").strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


def is_db_configured() -> bool:
    """Returns True if DATABASE_URL is configured."""
    return bool(get_database_url())


def get_connection():
    """
    Creates a new connection to Supabase PostgreSQL using psycopg2.
    Strictly cloud-only: NEVER falls back to SQLite or local files.
    """
    url = get_database_url()
    if not url:
        msg = (
            "CRITICAL: DATABASE_URL environment variable is missing. "
            "Supabase PostgreSQL is required. Local SQLite fallback has been completely removed "
            "to prevent data loss across Render deployments."
        )
        logger.critical(msg)
        raise RuntimeError(msg)

    try:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(
            url,
            cursor_factory=psycopg2.extras.RealDictCursor,
            connect_timeout=8
        )
        return conn
    except Exception as err:
        parsed = urlparse(url)
        host = parsed.hostname or "unknown"
        msg = (
            f"FATAL: Failed to connect to Supabase PostgreSQL at {host}: {err}. "
            "Make sure your DATABASE_URL is correct. If running on Render, ensure you are using "
            "the Supabase Connection Pooler URI (IPv4 supported) rather than direct IPv6."
        )
        logger.critical(msg)
        raise RuntimeError(msg) from err


@contextmanager
def get_db_cursor(commit: bool = False):
    """Context manager for safely executing queries and guaranteeing connection closure."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def check_db_health() -> Dict[str, Any]:
    """Tests the Supabase PostgreSQL connection and returns status dictionary."""
    url = get_database_url()
    if not url:
        return {
            "status": "error",
            "configured": False,
            "message": "DATABASE_URL environment variable is not configured."
        }

    try:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(url, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ping;")
        conn.close()

        parsed = urlparse(url)
        return {
            "status": "ok",
            "configured": True,
            "engine": "postgresql",
            "host": parsed.hostname,
            "database": parsed.path.lstrip("/"),
            "port": parsed.port
        }
    except Exception as err:
        return {
            "status": "error",
            "configured": True,
            "message": str(err)
        }


def init_db():
    """
    Initializes PostgreSQL tables and indexes on Supabase.
    Auto-seeds default content if the database is newly created and empty.
    """
    logger.info("Verifying and initializing Supabase PostgreSQL schema...")

    with get_db_cursor(commit=True) as cursor:
        # 1. Site Config Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                headline_word1 TEXT DEFAULT 'HAPPY',
                headline_word2 TEXT DEFAULT 'BIRTHDAY',
                giant_word TEXT DEFAULT 'YASH',
                top_badge TEXT DEFAULT 'NEXT LEVEL UI / UX',
                typing_text TEXT DEFAULT 'Wishing you a year of limitless innovation, relentless growth, and next-level milestones. Keep pushing the boundaries of excellence, YASH.',
                spec_pill1 TEXT DEFAULT 'CINEMATIC EDITION',
                spec_pill2 TEXT DEFAULT 'LEVEL 2026',
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Chapters Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chapters (
                id SERIAL PRIMARY KEY,
                step_index INTEGER NOT NULL UNIQUE,
                theme TEXT DEFAULT 'theme-crimson',
                badge TEXT NOT NULL,
                counter TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                media_type TEXT DEFAULT 'none',
                media_url TEXT DEFAULT '',
                media_name TEXT DEFAULT ''
            );
        """)

        # 3. Replies Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS replies (
                id SERIAL PRIMARY KEY,
                sender TEXT DEFAULT 'Glory',
                message TEXT NOT NULL,
                chapter_index INTEGER DEFAULT NULL,
                chapter_title TEXT DEFAULT '',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 4. Texts Table (Legacy support)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS texts (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                tag TEXT DEFAULT 'Inspire',
                style_preset TEXT DEFAULT 'minimal',
                font_size INTEGER DEFAULT 36,
                alignment TEXT DEFAULT 'center',
                glow INTEGER DEFAULT 1,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Performance Indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chapters_step_index ON chapters(step_index);
            CREATE INDEX IF NOT EXISTS idx_replies_created_at ON replies(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_replies_chapter_index ON replies(chapter_index);
        """)

        # Seed site_config if empty
        cursor.execute("SELECT COUNT(*) AS count FROM site_config WHERE id = 1;")
        count_row = cursor.fetchone()
        if not count_row or count_row["count"] == 0:
            cursor.execute("""
                INSERT INTO site_config (
                    id, headline_word1, headline_word2, giant_word, top_badge,
                    typing_text, spec_pill1, spec_pill2
                ) VALUES (
                    1, 'HAPPY', 'BIRTHDAY', 'YASH', 'NEXT LEVEL UI / UX',
                    'Wishing you a year of limitless innovation, relentless growth, and next-level milestones. Keep pushing the boundaries of excellence, YASH.',
                    'CINEMATIC EDITION', 'LEVEL 2026'
                ) ON CONFLICT (id) DO NOTHING;
            """)
            logger.info("Default site configuration seeded.")

        # Seed chapters if empty
        cursor.execute("SELECT COUNT(*) AS count FROM chapters;")
        chap_count = cursor.fetchone()
        if not chap_count or chap_count["count"] == 0:
            default_chapters = [
                (
                    0,
                    "theme-crimson",
                    "// CHAPTER 01",
                    "01 / 04",
                    "THE VISIONARY",
                    "Every masterpiece begins with bold vision. Your creativity, relentless drive, and dedication to excellence transform ideas into reality. Keep dreaming big, YASH.",
                    "none",
                    "",
                    ""
                ),
                (
                    1,
                    "theme-gold",
                    "// CHAPTER 02",
                    "02 / 04",
                    "UNSTOPPABLE DRIVE",
                    "Every challenge conquered has become another testament to your resilience. You continuously raise the standard and inspire everyone around you to aim higher.",
                    "none",
                    "",
                    ""
                ),
                (
                    2,
                    "theme-cyan",
                    "// CHAPTER 03",
                    "03 / 04",
                    "NEXT-LEVEL CRAFT",
                    "True mastery isn't just about reaching milestones—it's the relentless passion, precision, and infectious positive energy you bring to every endeavor.",
                    "none",
                    "",
                    ""
                ),
                (
                    3,
                    "theme-aurora",
                    "// FINALE CELEBRATION",
                    "04 / 04",
                    "THE FUTURE IS YOURS",
                    "Here is to another extraordinary year of breaking boundaries, unlocking new heights, and celebrating greatness. Happy Birthday, YASH! Keep shining!",
                    "none",
                    "",
                    ""
                )
            ]
            import psycopg2.extras
            psycopg2.extras.execute_values(
                cursor,
                """
                INSERT INTO chapters (
                    step_index, theme, badge, counter, title, body, media_type, media_url, media_name
                ) VALUES %s
                """,
                default_chapters
            )
            logger.info("Default chapters seeded into Supabase PostgreSQL.")

    logger.info("Supabase PostgreSQL schema initialization complete.")


# --- Site Config Operations ---
def get_site_config() -> Dict[str, Any]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM site_config WHERE id = 1;")
        row = cursor.fetchone()
        if row:
            return dict(row)

    return {
        "id": 1,
        "headline_word1": "HAPPY",
        "headline_word2": "BIRTHDAY",
        "giant_word": "YASH",
        "top_badge": "NEXT LEVEL UI / UX",
        "typing_text": "Wishing you a year of limitless innovation, relentless growth, and next-level milestones. Keep pushing the boundaries of excellence, YASH.",
        "spec_pill1": "CINEMATIC EDITION",
        "spec_pill2": "LEVEL 2026"
    }


def update_site_config(updates: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = [
        "headline_word1", "headline_word2", "giant_word",
        "top_badge", "typing_text", "spec_pill1", "spec_pill2"
    ]
    set_clauses = []
    values = []
    for k, v in updates.items():
        if k in allowed_fields and v is not None:
            set_clauses.append(f"{k} = %s")
            values.append(v)

    if not set_clauses:
        return get_site_config()

    set_clauses.append("updated_at = CURRENT_TIMESTAMP")
    sql = f"UPDATE site_config SET {', '.join(set_clauses)} WHERE id = 1"

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(sql, values)

    return get_site_config()


# --- Chapter Operations ---
def get_chapters() -> List[Dict[str, Any]]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM chapters ORDER BY step_index ASC;")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def get_chapter(step_index: int) -> Optional[Dict[str, Any]]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM chapters WHERE step_index = %s;", (step_index,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_chapter(step_index: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    allowed_fields = ["theme", "badge", "counter", "title", "body", "media_type", "media_url", "media_name"]
    set_clauses = []
    values = []
    for k, v in updates.items():
        if k in allowed_fields and v is not None:
            set_clauses.append(f"{k} = %s")
            values.append(v)

    if not set_clauses:
        return get_chapter(step_index)

    values.append(step_index)
    sql = f"UPDATE chapters SET {', '.join(set_clauses)} WHERE step_index = %s"

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(sql, values)

    return get_chapter(step_index)


def add_new_chapter(data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM chapters;")
        count = cursor.fetchone()["count"]
        next_idx = count
        total = count + 1

        theme = (data.get("theme") if data else None) or "theme-crimson"
        badge = (data.get("badge") if data else None) or f"// CHAPTER {total:02d}"
        counter = f"{total:02d} / {total:02d}"
        title = (data.get("title") if data else None) or "NEW MILESTONE"
        body = (data.get("body") if data else None) or "Every milestone is a testament to growth, relentless passion, and bold innovation. Keep shining bright, YASH."
        media_type = (data.get("media_type") if data else None) or "none"
        media_url = (data.get("media_url") if data else None) or ""
        media_name = (data.get("media_name") if data else None) or ""

        cursor.execute("""
            INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (next_idx, theme, badge, counter, title, body, media_type, media_url, media_name))

        # Update all chapter counters to reflect new total
        cursor.execute("SELECT id, step_index FROM chapters ORDER BY step_index ASC;")
        all_chaps = cursor.fetchall()
        for chap in all_chaps:
            new_counter = f"{chap['step_index'] + 1:02d} / {total:02d}"
            cursor.execute("UPDATE chapters SET counter = %s WHERE id = %s;", (new_counter, chap["id"]))

    return get_chapters()


def delete_chapter(step_index: int) -> List[Dict[str, Any]]:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM chapters WHERE step_index = %s;", (step_index,))

        cursor.execute("SELECT id FROM chapters ORDER BY step_index ASC;")
        remaining = cursor.fetchall()
        new_total = len(remaining)

        for new_idx, row in enumerate(remaining):
            new_counter = f"{new_idx + 1:02d} / {new_total:02d}"
            new_badge = f"// CHAPTER {new_idx + 1:02d}"
            cursor.execute("""
                UPDATE chapters 
                SET step_index = %s, counter = %s, badge = %s
                WHERE id = %s
            """, (new_idx, new_counter, new_badge, row["id"]))

    return get_chapters()


# --- Replies Operations ---
def add_reply(sender: str, message: str, chapter_index: Optional[int] = None, chapter_title: Optional[str] = None) -> Dict[str, Any]:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO replies (sender, message, chapter_index, chapter_title)
            VALUES (%s, %s, %s, %s)
            RETURNING id, sender, message, chapter_index, chapter_title, created_at;
        """, (sender.strip() or "Glory", message.strip(), chapter_index, chapter_title or ""))
        row = cursor.fetchone()
        return dict(row)


def get_replies() -> List[Dict[str, Any]]:
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                r.id, 
                r.sender, 
                r.message, 
                r.chapter_index,
                r.chapter_title,
                r.created_at,
                c.title AS card_title,
                c.badge AS card_badge,
                c.media_type,
                c.media_url,
                c.media_name
            FROM replies r
            LEFT JOIN chapters c ON r.chapter_index = c.step_index
            ORDER BY r.id DESC;
        """)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


# --- Texts Operations (Legacy Support) ---
def get_all_texts() -> List[Dict[str, Any]]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM texts ORDER BY id DESC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def add_text(content: str, tag: str = "Inspire", style_preset: str = "minimal",
             font_size: int = 36, alignment: str = "center", glow: int = 1) -> Dict[str, Any]:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO texts (content, tag, style_preset, font_size, alignment, glow)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, content, tag, style_preset, font_size, alignment, glow, created_at;
        """, (content.strip(), tag.strip() or "General", style_preset, font_size, alignment, glow))
        row = cursor.fetchone()
        return dict(row)


def delete_text(text_id: int) -> bool:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM texts WHERE id = %s;", (text_id,))
        return cursor.rowcount > 0


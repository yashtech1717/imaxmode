import os
import sqlite3
import logging
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger("aura.db")

DB_FILE = os.path.join(os.path.dirname(__file__), "texts.db")


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
    Connects to Supabase PostgreSQL when DATABASE_URL is provided.
    If DATABASE_URL is not set, gracefully uses local SQLite (texts.db)
    so local development runs smoothly without 500 errors.
    """
    url = get_database_url()
    if url:
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
            logger.warning(
                f"Could not connect to PostgreSQL ({err}). "
                "Using local SQLite database for this local session."
            )
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            return conn
    else:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn


def is_conn_postgres(conn) -> bool:
    return not isinstance(conn, sqlite3.Connection)


def q(sql: str, is_pg: bool) -> str:
    """Adapts query placeholders and syntax between PostgreSQL (%s) and SQLite (?)."""
    if is_pg:
        return sql
    # SQLite does not support RETURNING in older versions; strip if present
    clean_sql = sql
    if " RETURNING " in clean_sql.upper():
        clean_sql = clean_sql[:clean_sql.upper().rfind(" RETURNING ")]
    return clean_sql.replace("%s", "?")


def execute_insert(cursor, conn, sql: str, params: tuple) -> int:
    """Executes an INSERT and returns the newly generated ID for both PostgreSQL and SQLite."""
    if is_conn_postgres(conn):
        pg_sql = sql
        if " RETURNING " not in pg_sql.upper():
            pg_sql = pg_sql.rstrip(";") + " RETURNING id;"
        cursor.execute(pg_sql, params)
        row = cursor.fetchone()
        return row["id"] if row else 0
    else:
        sqlite_sql = q(sql, is_pg=False)
        cursor.execute(sqlite_sql, params)
        return cursor.lastrowid


@contextmanager
def get_db_cursor(commit: bool = False):
    """Context manager for safely executing queries and guaranteeing connection closure."""
    conn = get_connection()
    is_pg = is_conn_postgres(conn)
    try:
        cursor = conn.cursor()
        yield cursor, is_pg, conn
        if commit:
            conn.commit()
    except Exception:
        if hasattr(conn, "rollback"):
            conn.rollback()
        raise
    finally:
        conn.close()


def check_db_health() -> Dict[str, Any]:
    """Tests the database connection and returns status dictionary."""
    url = get_database_url()
    if not url:
        return {
            "status": "local_sqlite",
            "configured": False,
            "engine": "sqlite",
            "message": "DATABASE_URL not configured. Running on local SQLite texts.db."
        }

    try:
        import psycopg2
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
    """Initializes tables and indexes, seeding defaults only if empty."""
    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        if is_pg:
            logger.info("Initializing Supabase PostgreSQL schema...")
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

                CREATE TABLE IF NOT EXISTS replies (
                    id SERIAL PRIMARY KEY,
                    sender TEXT DEFAULT 'Glory',
                    message TEXT NOT NULL,
                    chapter_index INTEGER DEFAULT NULL,
                    chapter_title TEXT DEFAULT '',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );

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

                CREATE INDEX IF NOT EXISTS idx_chapters_step_index ON chapters(step_index);
                CREATE INDEX IF NOT EXISTS idx_replies_created_at ON replies(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_replies_chapter_index ON replies(chapter_index);
            """)
        else:
            logger.info("Initializing local SQLite schema (texts.db)...")
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
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chapters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT DEFAULT 'Glory',
                    message TEXT NOT NULL,
                    chapter_index INTEGER DEFAULT NULL,
                    chapter_title TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS texts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    tag TEXT DEFAULT 'Inspire',
                    style_preset TEXT DEFAULT 'minimal',
                    font_size INTEGER DEFAULT 36,
                    alignment TEXT DEFAULT 'center',
                    glow INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        # Seed site_config if empty
        cursor.execute("SELECT COUNT(*) AS count FROM site_config WHERE id = 1;")
        res = cursor.fetchone()
        count = res["count"] if res else 0
        if count == 0:
            cursor.execute("""
                INSERT INTO site_config (
                    id, headline_word1, headline_word2, giant_word, top_badge,
                    typing_text, spec_pill1, spec_pill2
                ) VALUES (
                    1, 'HAPPY', 'BIRTHDAY', 'YASH', 'NEXT LEVEL UI / UX',
                    'Wishing you a year of limitless innovation, relentless growth, and next-level milestones. Keep pushing the boundaries of excellence, YASH.',
                    'CINEMATIC EDITION', 'LEVEL 2026'
                );
            """)

        # Seed chapters if empty
        cursor.execute("SELECT COUNT(*) AS count FROM chapters;")
        res = cursor.fetchone()
        chap_count = res["count"] if res else 0
        if chap_count == 0:
            default_chapters = [
                (0, "theme-crimson", "// CHAPTER 01", "01 / 04", "THE VISIONARY", "Every masterpiece begins with bold vision. Your creativity, relentless drive, and dedication to excellence transform ideas into reality. Keep dreaming big, YASH.", "none", "", ""),
                (1, "theme-gold", "// CHAPTER 02", "02 / 04", "UNSTOPPABLE DRIVE", "Every challenge conquered has become another testament to your resilience. You continuously raise the standard and inspire everyone around you to aim higher.", "none", "", ""),
                (2, "theme-cyan", "// CHAPTER 03", "03 / 04", "NEXT-LEVEL CRAFT", "True mastery isn't just about reaching milestones—it's the relentless passion, precision, and infectious positive energy you bring to every endeavor.", "none", "", ""),
                (3, "theme-aurora", "// FINALE CELEBRATION", "04 / 04", "THE FUTURE IS YOURS", "Here is to another extraordinary year of breaking boundaries, unlocking new heights, and celebrating greatness. Happy Birthday, YASH! Keep shining!", "none", "", "")
            ]
            if is_pg:
                import psycopg2.extras
                psycopg2.extras.execute_values(
                    cursor,
                    "INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name) VALUES %s",
                    default_chapters
                )
            else:
                cursor.executemany(
                    "INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    default_chapters
                )


# --- Site Config Operations ---
def get_site_config() -> Dict[str, Any]:
    with get_db_cursor() as (cursor, is_pg, conn):
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

    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        cursor.execute(q(sql, is_pg), values)

    return get_site_config()


# --- Chapter Operations ---
def get_chapters() -> List[Dict[str, Any]]:
    with get_db_cursor() as (cursor, is_pg, conn):
        cursor.execute("SELECT * FROM chapters ORDER BY step_index ASC;")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def get_chapter(step_index: int) -> Optional[Dict[str, Any]]:
    with get_db_cursor() as (cursor, is_pg, conn):
        cursor.execute(q("SELECT * FROM chapters WHERE step_index = %s;", is_pg), (step_index,))
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

    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        cursor.execute(q(sql, is_pg), values)

    return get_chapter(step_index)


def add_new_chapter(data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        cursor.execute("SELECT COUNT(*) AS count FROM chapters;")
        res = cursor.fetchone()
        count = res["count"] if res else 0
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

        cursor.execute(q("""
            INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, is_pg), (next_idx, theme, badge, counter, title, body, media_type, media_url, media_name))

        # Update all chapter counters
        cursor.execute("SELECT id, step_index FROM chapters ORDER BY step_index ASC;")
        all_chaps = cursor.fetchall()
        for chap in all_chaps:
            new_counter = f"{chap['step_index'] + 1:02d} / {total:02d}"
            cursor.execute(q("UPDATE chapters SET counter = %s WHERE id = %s;", is_pg), (new_counter, chap["id"]))

    return get_chapters()


def delete_chapter(step_index: int) -> List[Dict[str, Any]]:
    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        cursor.execute(q("DELETE FROM chapters WHERE step_index = %s;", is_pg), (step_index,))

        cursor.execute("SELECT id FROM chapters ORDER BY step_index ASC;")
        remaining = cursor.fetchall()
        new_total = len(remaining)

        for new_idx, row in enumerate(remaining):
            new_counter = f"{new_idx + 1:02d} / {new_total:02d}"
            new_badge = f"// CHAPTER {new_idx + 1:02d}"
            cursor.execute(q("""
                UPDATE chapters 
                SET step_index = %s, counter = %s, badge = %s
                WHERE id = %s
            """, is_pg), (new_idx, new_counter, new_badge, row["id"]))

    return get_chapters()


# --- Replies Operations ---
def add_reply(sender: str, message: str, chapter_index: Optional[int] = None, chapter_title: Optional[str] = None) -> Dict[str, Any]:
    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        new_id = execute_insert(
            cursor,
            conn,
            """
            INSERT INTO replies (sender, message, chapter_index, chapter_title)
            VALUES (%s, %s, %s, %s)
            """,
            (sender.strip() or "Glory", message.strip(), chapter_index, chapter_title or "")
        )
        cursor.execute(q("SELECT * FROM replies WHERE id = %s;", is_pg), (new_id,))
        row = cursor.fetchone()
        return dict(row)


def get_replies() -> List[Dict[str, Any]]:
    with get_db_cursor() as (cursor, is_pg, conn):
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
    with get_db_cursor() as (cursor, is_pg, conn):
        cursor.execute("SELECT * FROM texts ORDER BY id DESC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def add_text(content: str, tag: str = "Inspire", style_preset: str = "minimal",
             font_size: int = 36, alignment: str = "center", glow: int = 1) -> Dict[str, Any]:
    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        new_id = execute_insert(
            cursor,
            conn,
            """
            INSERT INTO texts (content, tag, style_preset, font_size, alignment, glow)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (content.strip(), tag.strip() or "General", style_preset, font_size, alignment, glow)
        )
        cursor.execute(q("SELECT * FROM texts WHERE id = %s;", is_pg), (new_id,))
        row = cursor.fetchone()
        return dict(row)


def delete_text(text_id: int) -> bool:
    with get_db_cursor(commit=True) as (cursor, is_pg, conn):
        cursor.execute(q("DELETE FROM texts WHERE id = %s;", is_pg), (text_id,))
        return cursor.rowcount > 0

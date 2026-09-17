import sqlite3
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("aura.db")

DB_FILE = os.path.join(os.path.dirname(__file__), "texts.db")
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# Normalize Render/Heroku postgres:// to postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

IS_POSTGRES = bool(DATABASE_URL)

def get_connection():
    if IS_POSTGRES:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
        return conn
    else:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

def q(sql: str) -> str:
    """Translates SQLite '?' parameter placeholders to PostgreSQL '%s' when needed."""
    if IS_POSTGRES:
        return sql.replace("?", "%s")
    return sql

def execute_insert(cursor, sql: str, params: tuple) -> int:
    """Executes an INSERT statement and returns the newly generated ID for both engines."""
    if IS_POSTGRES:
        cursor.execute(q(sql) + " RETURNING id", params)
        row = cursor.fetchone()
        return row["id"] if row else 0
    else:
        cursor.execute(sql, params)
        return cursor.lastrowid

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    if IS_POSTGRES:
        logger.info("Initializing PostgreSQL Cloud Database schema...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS texts (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                tag TEXT DEFAULT 'Inspire',
                style_preset TEXT DEFAULT 'minimal',
                font_size INTEGER DEFAULT 36,
                alignment TEXT DEFAULT 'center',
                glow INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            ALTER TABLE replies ADD COLUMN IF NOT EXISTS chapter_index INTEGER DEFAULT NULL;
            ALTER TABLE replies ADD COLUMN IF NOT EXISTS chapter_title TEXT DEFAULT '';
        """)
        conn.commit()
    else:
        logger.info("Initializing local SQLite Database schema...")
        # Legacy texts table
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
            )
        """)

        # 1. Site configuration table (Hero text, typewriter, backdrop)
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
            )
        """)

        # 2. Chapters table (Dot cards, text, attached media)
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
            )
        """)

        # 3. Replies table (Messages sent from Glory to Yash)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT DEFAULT 'Glory',
                message TEXT NOT NULL,
                chapter_index INTEGER DEFAULT NULL,
                chapter_title TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # Migration for existing replies table if columns missing
        cursor.execute("PRAGMA table_info(replies)")
        existing_cols = [row["name"] for row in cursor.fetchall()]
        if "chapter_index" not in existing_cols:
            cursor.execute("ALTER TABLE replies ADD COLUMN chapter_index INTEGER DEFAULT NULL")
        if "chapter_title" not in existing_cols:
            cursor.execute("ALTER TABLE replies ADD COLUMN chapter_title TEXT DEFAULT ''")
        conn.commit()

    # Seed site_config if empty
    cursor.execute("SELECT COUNT(*) as count FROM site_config WHERE id = 1")
    count_row = cursor.fetchone()
    if count_row["count"] == 0:
        cursor.execute("""
            INSERT INTO site_config (id, headline_word1, headline_word2, giant_word, top_badge, typing_text, spec_pill1, spec_pill2)
            VALUES (1, 'HAPPY', 'BIRTHDAY', 'YASH', 'NEXT LEVEL UI / UX',
                    'Wishing you a year of limitless innovation, relentless growth, and next-level milestones. Keep pushing the boundaries of excellence, YASH.',
                    'CINEMATIC EDITION', 'LEVEL 2026')
        """)
        conn.commit()

    # Seed chapters if empty
    cursor.execute("SELECT COUNT(*) as count FROM chapters")
    if cursor.fetchone()["count"] == 0:
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
        if IS_POSTGRES:
            import psycopg2.extras
            psycopg2.extras.execute_values(
                cursor,
                "INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name) VALUES %s",
                default_chapters
            )
        else:
            cursor.executemany("""
                INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, default_chapters)
        conn.commit()

    conn.close()

# --- Site Config Operations ---
def get_site_config() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM site_config WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
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
            set_clauses.append(f"{k} = ?")
            values.append(v)

    if not set_clauses:
        return get_site_config()

    set_clauses.append("updated_at = CURRENT_TIMESTAMP")
    sql = f"UPDATE site_config SET {', '.join(set_clauses)} WHERE id = 1"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(q(sql), values)
    conn.commit()
    conn.close()
    return get_site_config()

# --- Chapter Operations ---
def get_chapters() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chapters ORDER BY step_index ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_chapter(step_index: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(q("SELECT * FROM chapters WHERE step_index = ?"), (step_index,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_chapter(step_index: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    allowed_fields = ["theme", "badge", "counter", "title", "body", "media_type", "media_url", "media_name"]
    set_clauses = []
    values = []
    for k, v in updates.items():
        if k in allowed_fields and v is not None:
            set_clauses.append(f"{k} = ?")
            values.append(v)

    if not set_clauses:
        return get_chapter(step_index)

    values.append(step_index)
    sql = f"UPDATE chapters SET {', '.join(set_clauses)} WHERE step_index = ?"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(q(sql), values)
    conn.commit()
    conn.close()
    return get_chapter(step_index)

def add_new_chapter(data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM chapters")
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

    cursor.execute(q("""
        INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """), (next_idx, theme, badge, counter, title, body, media_type, media_url, media_name))

    # Update all chapter counters to reflect new total
    cursor.execute("SELECT id, step_index FROM chapters ORDER BY step_index ASC")
    all_chaps = cursor.fetchall()
    for chap in all_chaps:
        new_counter = f"{chap['step_index'] + 1:02d} / {total:02d}"
        cursor.execute(q("UPDATE chapters SET counter = ? WHERE id = ?"), (new_counter, chap["id"]))

    conn.commit()
    conn.close()
    return get_chapters()

def delete_chapter(step_index: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(q("DELETE FROM chapters WHERE step_index = ?"), (step_index,))
    
    # Fetch remaining chapters ordered by old step_index
    cursor.execute("SELECT id FROM chapters ORDER BY step_index ASC")
    remaining = cursor.fetchall()
    new_total = len(remaining)

    for new_idx, row in enumerate(remaining):
        new_counter = f"{new_idx + 1:02d} / {new_total:02d}"
        new_badge = f"// CHAPTER {new_idx + 1:02d}"
        cursor.execute(q("""
            UPDATE chapters 
            SET step_index = ?, counter = ?, badge = ?
            WHERE id = ?
        """), (new_idx, new_counter, new_badge, row["id"]))

    conn.commit()
    conn.close()
    return get_chapters()

# --- Replies Operations ---
def add_reply(sender: str, message: str, chapter_index: Optional[int] = None, chapter_title: Optional[str] = None) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    new_id = execute_insert(
        cursor,
        """
        INSERT INTO replies (sender, message, chapter_index, chapter_title)
        VALUES (?, ?, ?, ?)
        """,
        (sender.strip() or "Glory", message.strip(), chapter_index, chapter_title or "")
    )
    conn.commit()
    cursor.execute(q("SELECT * FROM replies WHERE id = ?"), (new_id,))
    reply = dict(cursor.fetchone())
    conn.close()
    return reply

def get_replies() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            r.id, 
            r.sender, 
            r.message, 
            r.chapter_index,
            r.chapter_title,
            r.created_at,
            c.title as card_title,
            c.badge as card_badge,
            c.media_type,
            c.media_url,
            c.media_name
        FROM replies r
        LEFT JOIN chapters c ON r.chapter_index = c.step_index
        ORDER BY r.id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Legacy Text operations ---
def get_all_texts() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM texts ORDER BY id DESC")
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results

def add_text(content: str, tag: str = "Inspire", style_preset: str = "minimal",
             font_size: int = 36, alignment: str = "center", glow: int = 1) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    new_id = execute_insert(
        cursor,
        """
        INSERT INTO texts (content, tag, style_preset, font_size, alignment, glow)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (content.strip(), tag.strip() or "General", style_preset, font_size, alignment, glow)
    )
    conn.commit()
    cursor.execute(q("SELECT * FROM texts WHERE id = ?"), (new_id,))
    new_record = dict(cursor.fetchone())
    conn.close()
    return new_record

def delete_text(text_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(q("DELETE FROM texts WHERE id = ?"), (text_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


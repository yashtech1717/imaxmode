-- ==============================================================================
-- AURA CINEMATIC PORTAL // SUPABASE POSTGRESQL SCHEMA & STORAGE CONFIGURATION
-- ==============================================================================
-- Run this SQL in your Supabase Dashboard -> SQL Editor (or let the app auto-initialize)

-- 1. Site Configuration Table (Hero Headlines, Typewriter Story, Giant Backdrop)
CREATE TABLE IF NOT EXISTS site_config (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    headline_word1 TEXT NOT NULL DEFAULT 'HAPPY',
    headline_word2 TEXT NOT NULL DEFAULT 'BIRTHDAY',
    giant_word TEXT NOT NULL DEFAULT 'YASH',
    top_badge TEXT NOT NULL DEFAULT 'NEXT LEVEL UI / UX',
    typing_text TEXT NOT NULL DEFAULT 'Wishing you a year of limitless innovation, relentless growth, and next-level milestones. Keep pushing the boundaries of excellence, YASH.',
    spec_pill1 TEXT NOT NULL DEFAULT 'CINEMATIC EDITION',
    spec_pill2 TEXT NOT NULL DEFAULT 'LEVEL 2026',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed default site configuration if empty
INSERT INTO site_config (id, headline_word1, headline_word2, giant_word, top_badge, typing_text, spec_pill1, spec_pill2)
VALUES (1, 'HAPPY', 'BIRTHDAY', 'YASH', 'NEXT LEVEL UI / UX',
        'Wishing you a year of limitless innovation, relentless growth, and next-level milestones. Keep pushing the boundaries of excellence, YASH.',
        'CINEMATIC EDITION', 'LEVEL 2026')
ON CONFLICT (id) DO NOTHING;

-- 2. Chapter Cards Table (Milestone cards, Badges, Counters, Attached Media)
CREATE TABLE IF NOT EXISTS chapters (
    id SERIAL PRIMARY KEY,
    step_index INTEGER NOT NULL UNIQUE,
    theme TEXT NOT NULL DEFAULT 'theme-crimson',
    badge TEXT NOT NULL,
    counter TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    media_type TEXT NOT NULL DEFAULT 'none',
    media_url TEXT NOT NULL DEFAULT '',
    media_name TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chapters_step_index ON chapters(step_index ASC);

-- Seed default 4 chapters if table is empty
INSERT INTO chapters (step_index, theme, badge, counter, title, body, media_type, media_url, media_name)
VALUES 
(
    0, 'theme-crimson', '// CHAPTER 01', '01 / 04', 'THE VISIONARY',
    'Every masterpiece begins with bold vision. Your creativity, relentless drive, and dedication to excellence transform ideas into reality. Keep dreaming big, YASH.',
    'none', '', ''
),
(
    1, 'theme-gold', '// CHAPTER 02', '02 / 04', 'UNSTOPPABLE DRIVE',
    'Every challenge conquered has become another testament to your resilience. You continuously raise the standard and inspire everyone around you to aim higher.',
    'none', '', ''
),
(
    2, 'theme-cyan', '// CHAPTER 03', '03 / 04', 'NEXT-LEVEL CRAFT',
    'True mastery isn''t just about reaching milestones—it''s the relentless passion, precision, and infectious positive energy you bring to every endeavor.',
    'none', '', ''
),
(
    3, 'theme-aurora', '// FINALE CELEBRATION', '04 / 04', 'THE FUTURE IS YOURS',
    'Here is to another extraordinary year of breaking boundaries, unlocking new heights, and celebrating greatness. Happy Birthday, YASH! Keep shining!',
    'none', '', ''
)
ON CONFLICT (step_index) DO NOTHING;

-- 3. Replies Table (Messages sent from Viewer / Glory to Admin / Yash)
CREATE TABLE IF NOT EXISTS replies (
    id SERIAL PRIMARY KEY,
    sender TEXT NOT NULL DEFAULT 'Glory',
    message TEXT NOT NULL,
    chapter_index INTEGER DEFAULT NULL,
    chapter_title TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_replies_chapter_index ON replies(chapter_index);
CREATE INDEX IF NOT EXISTS idx_replies_created_at ON replies(created_at DESC);

-- 4. Legacy Texts Table (Backward compatibility)
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

-- ==============================================================================
-- SUPABASE STORAGE BUCKET CONFIGURATION
-- ==============================================================================
-- 1. Create the 'memories' bucket for permanent media storage (Photos, Videos, Audio)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'memories',
    'memories',
    TRUE,
    52428800, -- 50MB per individual file limit (1GB total free storage)
    ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'video/mp4', 'video/webm', 'video/quicktime', 'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4']
)
ON CONFLICT (id) DO UPDATE SET public = TRUE;

-- 2. Storage Policies: Allow public read access to all objects in 'memories' bucket
CREATE POLICY "Public Read Access"
ON storage.objects FOR SELECT
USING (bucket_id = 'memories');

-- 3. Storage Policies: Allow authenticated and service_role inserts into 'memories' bucket
CREATE POLICY "Allow Uploads"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'memories');

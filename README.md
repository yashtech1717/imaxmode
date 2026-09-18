# AURA // Cinematic Birthday Canvas & Portal

A luxury cinematic web experience with dual role interfaces:
- **Yash (Admin CMS)**: Real-time customization of headlines, typewriter text, chapters, media uploads, and reply inbox.
- **Glory (Viewer)**: Interactive 4-chapter narrative presentation, sound synthesizer, rich media attachments, and contextual replies.

All data (chapters, configuration, replies) is **permanently persisted in Supabase PostgreSQL**, and all media uploads (photos, audio, videos) are **stored permanently in Supabase Storage**. Local SQLite and Render ephemeral filesystem storage have been completely removed.

---

## ⚡ Architecture & Cloud Persistence

| Layer | Technology | Storage Destination |
| :--- | :--- | :--- |
| **Backend** | FastAPI (Python 3.10) | Render Web Service |
| **Database** | Supabase PostgreSQL (`psycopg2`) | Permanent Cloud Database |
| **Media Storage**| Supabase Storage Bucket (`memories`) | Permanent Cloud CDN |
| **Frontend** | Vanilla JS, Web Audio API, Canvas | Dynamic Responsive OLED Black UI |

> [!IMPORTANT]
> **No Ephemeral Data Loss**: All state is stored in Supabase. Redeploying, restarting, or scaling the Render instance will never lose chapters, messages, or uploaded media.

---

## 🚀 Environment Configuration

Add these environment variables to your Render Service Dashboard or local `.env`:

```bash
# 1. Supabase PostgreSQL URI (Connection Pooler required for Render IPv4 compatibility)
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

# 2. Supabase Storage API
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_KEY=[your-supabase-service-role-or-anon-key]
SUPABASE_BUCKET=memories

# 3. Server Port (Render sets this automatically)
PORT=8000
```

---

## 🛠️ Database Setup & Migration

### 1. Execute SQL Schema in Supabase
Run the contents of `supabase_schema.sql` in the **Supabase Dashboard -> SQL Editor**:
- Creates `site_config`, `chapters`, `replies`, and `texts` tables.
- Creates indexes and public storage policies for the `memories` bucket.

### 2. Migrate Existing Local Data (Optional)
If you have data in a local `texts.db` or files in `static/uploads/`, migrate them to Supabase:
```bash
python migrate_sqlite_to_supabase.py
```
This script uploads local videos/photos to your Supabase Storage bucket and upserts all chapters, replies, and texts into Supabase PostgreSQL.

---

## 🩺 Health Check & Monitoring

The application provides dual health check endpoints:
- `GET /health`
- `GET /api/health`

Returns real-time connection status for both Supabase Database and Supabase Storage:
```json
{
  "status": "healthy",
  "service": "AURA Cinematic Portal",
  "version": "2.0.0",
  "storage_mode": "supabase",
  "database": {
    "status": "ok",
    "configured": true,
    "engine": "postgresql",
    "host": "aws-0-ap-south-1.pooler.supabase.com"
  },
  "storage": {
    "status": "ok",
    "configured": true,
    "bucket": "memories",
    "public": true
  }
}
```

---

## 🧪 Testing

Run the test suite locally:
```bash
python test_app.py
```
Validates:
- Strict refusal of SQLite fallback when `DATABASE_URL` is missing.
- Strict refusal of local file writes when `SUPABASE_URL` is missing.
- Health endpoint reporting `"storage_mode": "supabase"`.
- Authentication (Yash admin credentials, Glory viewer login variants).
- Cloud upload and CDN URL generation.

---

## 📁 Project Structure

```
uiux/
├── main.py                       # FastAPI server, REST API, startup cloud checks
├── db.py                         # Strict Supabase PostgreSQL engine (psycopg2)
├── cloud_storage.py              # Supabase Storage bucket client (REST API)
├── supabase_schema.sql           # Complete PostgreSQL DDL & Storage RLS policies
├── migrate_sqlite_to_supabase.py # SQLite to Supabase migration tool
├── test_app.py                   # Automated test suite
├── render.yaml                   # Render deployment configuration
├── Procfile                      # Render start command
├── requirements.txt              # Production dependencies
├── .env.example                  # Environment variable reference
├── templates/
│   └── index.html                # Cinematic OLED UI
└── static/
    ├── css/
    │   └── style.css             # Glassmorphism, animations, Supernova styling
    └── js/
        └── app.js                # Chapter slider, audio synth, Supabase upload integration
```

# AURA // Minimalist Text Showcase Website

A sleek, modern Python full-stack web application featuring an ultra-clean obsidian/black background and exceptional UI/UX for displaying, styling, and managing texts, quotes, and statements.

## ✨ Features

- **Clean Obsidian Aesthetic**: Deep `#050507` background with subtle micro-grid overlay and dynamic ambient mouse spotlight glow.
- **Hero Text Showcase**: High-impact text stage with smooth animated transitions.
- **5 Typography Presets**:
  - **Obsidian**: Modern, crisp sans-serif with specular white glow.
  - **Editorial**: Luxury magazine serif with subtle italic phrasing.
  - **Cyber Glow**: Vibrant electric cyan and purple drop-shadow glow.
  - **Terminal**: JetBrains Mono typewriter block with simulated code styling.
  - **Aurora**: Dreamy pastel gradient text shimmer.
- **Real-Time Reactive Customizer**:
  - Instant live preview as you type.
  - Interactive font size slider (20px - 72px).
  - Left / Center / Right alignment switches.
  - Ambient glow toggle.
  - Category tags (e.g. `#Philosophy`, `#Design`, `#Code`).
- **Quick Utility Actions**:
  - One-click copy to clipboard with toast notification.
  - **Export Card Image**: Generates and downloads high-resolution PNG cards using HTML5 Canvas.
  - **Zen Fullscreen Mode**: Immersive distraction-free reading experience (`Esc` to exit).
  - **Inspiration Randomizer**: Instantly cycles curated quotes.
- **Python Full-Stack & Persistent Storage**:
  - **FastAPI** backend with RESTful endpoints (`/api/texts`).
  - Built-in **SQLite** database (`texts.db`) to store and retrieve your saved texts.
  - Automatic interactive Swagger documentation available at `/docs`.

## 🚀 Getting Started

### 1. Requirements
Python 3.10+ with FastAPI, Uvicorn, and Jinja2 (already installed in your environment):
```bash
pip install -r requirements.txt
```

### 2. Run the Application
You can run the server directly using the launcher:
```bash
python run.py
```
Or with Uvicorn:
```bash
python -m uvicorn main:app --reload --port 8000
```

### 3. Open in Browser
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📁 Project Structure

```
uiux/
├── main.py              # FastAPI server & REST API
├── db.py                # SQLite database management
├── run.py               # One-click launcher with auto-browser opening
├── requirements.txt     # Dependency list
├── templates/
│   └── index.html       # Clean semantic HTML5 layout
├── static/
│   ├── css/
│   │   └── style.css    # Clean obsidian dark design system
│   └── js/
│       └── app.js       # Live preview engine & API client
└── texts.db             # Generated SQLite database file
```

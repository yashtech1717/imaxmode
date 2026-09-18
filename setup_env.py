"""
AURA // Interactive Supabase Environment Setup Helper
=====================================================
Run with:
    python setup_env.py

Prompts you for your Supabase credentials, writes them safely to .env,
and immediately verifies them with the diagnostic engine.
"""

import os
import sys

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diagnostic import run_supabase_diagnostic, format_diagnostic_text

ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


def main():
    print("=" * 65)
    print("  ✦ AURA // SUPABASE CREDENTIAL CONFIGURATOR")
    print("=" * 65)
    print("This tool safely saves your credentials to a local .env file")
    print("(which is gitignored and will never be pushed to GitHub).\n")

    current_url = os.environ.get("SUPABASE_URL", "")
    current_key = os.environ.get("SUPABASE_KEY", "")
    current_db = os.environ.get("DATABASE_URL", "")

    # 1. Prompt for SUPABASE_URL
    print("[Step 1/3] Supabase Project URL")
    print("Find this in: Supabase Dashboard -> Project Settings -> API")
    url_prompt = f"Enter SUPABASE_URL [{current_url}]: " if current_url else "Enter SUPABASE_URL (e.g. https://xxx.supabase.co): "
    url_input = input(url_prompt).strip()
    supabase_url = url_input or current_url

    if not supabase_url:
        print("[!] SUPABASE_URL cannot be empty.")
        return

    if not supabase_url.startswith("http://") and not supabase_url.startswith("https://"):
        supabase_url = "https://" + supabase_url
    supabase_url = supabase_url.rstrip("/")

    # 2. Prompt for SUPABASE_KEY
    print("\n[Step 2/3] Supabase API Key (anon or service_role)")
    print("Find this in: Supabase Dashboard -> Project Settings -> API -> Project API Keys")
    key_prompt = "Enter SUPABASE_KEY: "
    key_input = input(key_prompt).strip()
    supabase_key = key_input or current_key

    if not supabase_key:
        print("[!] SUPABASE_KEY cannot be empty.")
        return

    # 3. Prompt for DATABASE_URL (Optional)
    print("\n[Step 3/3] Supabase Database Connection URI (Optional)")
    print("Find this in: Supabase Dashboard -> Project Settings -> Database -> Connection string (URI)")
    db_prompt = f"Enter DATABASE_URL (or press Enter to skip): "
    db_input = input(db_prompt).strip()
    database_url = db_input or current_db

    # Write to .env
    lines = [
        "# AURA Portal Local Environment Variables",
        f"SUPABASE_URL={supabase_url}",
        f"SUPABASE_KEY={supabase_key}",
        "SUPABASE_BUCKET=memories",
    ]
    if database_url:
        lines.append(f"DATABASE_URL={database_url}")
    lines.append("PORT=8000\n")

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[OK] Successfully saved configuration to {ENV_FILE}!")

    # Set in memory for immediate test
    os.environ["SUPABASE_URL"] = supabase_url
    os.environ["SUPABASE_KEY"] = supabase_key
    os.environ["SUPABASE_BUCKET"] = "memories"
    if database_url:
        os.environ["DATABASE_URL"] = database_url

    print("\nRunning diagnostic verification now...\n")
    results = run_supabase_diagnostic()
    print(format_diagnostic_text(results))

    if results.get("overall_status") == "SUCCESS":
        print("\n[SUCCESS] All Supabase credentials verified successfully!")
        print("Now when you run 'python run.py', it will automatically load your credentials.")
    else:
        print("\n[NOTICE] Check the REASON above to adjust any values in your .env file.")


if __name__ == "__main__":
    main()

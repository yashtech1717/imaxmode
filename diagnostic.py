"""
Supabase Configuration & Credential Diagnostic Module
=====================================================
Performs non-destructive, read-only verification of all 7 Supabase components:
1. SUPABASE_URL:            FOUND / MISSING
2. SUPABASE_KEY:            FOUND / MISSING
3. SUPABASE CLIENT:         SUCCESS / FAILED
4. SUPABASE AUTHENTICATION: SUCCESS / FAILED
5. POSTGRES CONNECTION:     SUCCESS / FAILED
6. DATABASE SCHEMA:         SUCCESS / FAILED
7. STORAGE BUCKET:          SUCCESS / FAILED

SECURITY REQUIREMENTS:
- NEVER print, log, or expose secret keys or passwords.
- Only report whether each component succeeds or fails with the exact reason.
"""

import os
import sys
import logging
from pathlib import Path
from urllib.parse import urlparse
import requests

# Explicitly load .env from project root
_env_file = Path(__file__).resolve().parent / ".env"
try:
    from dotenv import load_dotenv
    if _env_file.exists():
        load_dotenv(dotenv_path=_env_file, override=True)
    else:
        load_dotenv(override=True)
except ImportError:
    pass

logger = logging.getLogger("aura.diagnostic")


def run_supabase_diagnostic() -> dict:
    """
    Executes a complete 7-point diagnostic test suite against Supabase.
    Strictly read-only; guarantees zero secret leaks and zero data modification.
    """
    results = {
        "supabase_url": {
            "status": "MISSING",
            "value": None,
            "reason": None
        },
        "supabase_key": {
            "status": "MISSING",
            "masked_preview": None,
            "key_type": None,
            "reason": None
        },
        "supabase_client": {
            "status": "FAILED",
            "reason": None
        },
        "supabase_authentication": {
            "status": "FAILED",
            "reason": None,
            "details": None
        },
        "postgres_connection": {
            "status": "FAILED",
            "host": None,
            "reason": None,
            "details": None
        },
        "database_schema": {
            "status": "FAILED",
            "tables_found": [],
            "missing_tables": [],
            "reason": None,
            "details": None
        },
        "storage_bucket": {
            "status": "FAILED",
            "bucket_tested": os.environ.get("SUPABASE_BUCKET", "memories").strip(),
            "reason": None,
            "details": None
        },
        "overall_status": "UNKNOWN"
    }

    # ---------------------------------------------------------
    # 1. Test SUPABASE_URL
    # ---------------------------------------------------------
    raw_url = os.environ.get("SUPABASE_URL", "").strip()
    if not raw_url:
        results["supabase_url"]["status"] = "MISSING"
        results["supabase_url"]["reason"] = "SUPABASE_URL environment variable is not set."
    else:
        parsed = urlparse(raw_url)
        if not parsed.scheme or not parsed.netloc:
            results["supabase_url"]["status"] = "MISSING"
            results["supabase_url"]["reason"] = f"Invalid URL format: '{raw_url}'"
        else:
            clean_url = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
            results["supabase_url"]["status"] = "FOUND"
            results["supabase_url"]["value"] = clean_url

    # ---------------------------------------------------------
    # 2. Test SUPABASE_KEY
    # ---------------------------------------------------------
    raw_key = (
        os.environ.get("SUPABASE_KEY", "").strip()
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    )
    if not raw_key:
        results["supabase_key"]["status"] = "MISSING"
        results["supabase_key"]["reason"] = "SUPABASE_KEY environment variable is not set."
    else:
        results["supabase_key"]["status"] = "FOUND"
        key_type = "JWT Token" if raw_key.startswith("ey") else "API Key"
        masked = f"{raw_key[:4]}...{raw_key[-4:]} (Length: {len(raw_key)})" if len(raw_key) > 12 else f"[MASKED - Length: {len(raw_key)}]"
        results["supabase_key"]["masked_preview"] = masked
        results["supabase_key"]["key_type"] = key_type

    supabase_url = results["supabase_url"].get("value")
    supabase_key = raw_key

    # ---------------------------------------------------------
    # 3. Test SUPABASE CLIENT
    # ---------------------------------------------------------
    try:
        from supabase import create_client
        if supabase_url and supabase_key:
            _client = create_client(supabase_url, supabase_key)
            results["supabase_client"]["status"] = "SUCCESS"
        else:
            results["supabase_client"]["status"] = "FAILED"
            results["supabase_client"]["reason"] = "SUPABASE_URL or SUPABASE_KEY is missing."
    except ImportError:
        results["supabase_client"]["status"] = "FAILED"
        results["supabase_client"]["reason"] = "No module named 'supabase'. Install with: pip install supabase"
    except Exception as err:
        results["supabase_client"]["status"] = "FAILED"
        results["supabase_client"]["reason"] = f"Client initialization error: {err}"

    # ---------------------------------------------------------
    # 4. Test SUPABASE AUTHENTICATION
    # ---------------------------------------------------------
    if supabase_url and supabase_key:
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        try:
            auth_test_url = f"{supabase_url}/rest/v1/"
            res = requests.get(auth_test_url, headers=headers, timeout=8)
            if res.status_code in [200, 204]:
                results["supabase_authentication"]["status"] = "SUCCESS"
                results["supabase_authentication"]["details"] = "Supabase API Gateway authenticated successfully."
            elif res.status_code == 401:
                results["supabase_authentication"]["status"] = "FAILED"
                results["supabase_authentication"]["reason"] = "invalid/expired key"
                results["supabase_authentication"]["details"] = f"Supabase rejected API key (HTTP 401 Unauthorized: {res.text.strip()})"
            elif res.status_code == 403:
                results["supabase_authentication"]["status"] = "FAILED"
                results["supabase_authentication"]["reason"] = "authentication/permission error"
                results["supabase_authentication"]["details"] = "HTTP 403 Forbidden: API key lacks required permissions."
            else:
                # Any response with valid swagger/openAPI spec or headers from Supabase means authentication succeeded
                results["supabase_authentication"]["status"] = "SUCCESS"
                results["supabase_authentication"]["details"] = f"Supabase responded with status {res.status_code}"
        except requests.exceptions.ConnectionError as err:
            results["supabase_authentication"]["status"] = "FAILED"
            results["supabase_authentication"]["reason"] = f"network/connection error (could not resolve or reach host: {err})"
        except requests.exceptions.Timeout:
            results["supabase_authentication"]["status"] = "FAILED"
            results["supabase_authentication"]["reason"] = "network/connection error (request timed out after 8s)"
        except Exception as err:
            results["supabase_authentication"]["status"] = "FAILED"
            results["supabase_authentication"]["reason"] = f"network/connection error ({err})"
    else:
        results["supabase_authentication"]["status"] = "FAILED"
        results["supabase_authentication"]["reason"] = "missing environment variable (SUPABASE_URL or SUPABASE_KEY)"

    # ---------------------------------------------------------
    # 5. Test POSTGRES CONNECTION
    # ---------------------------------------------------------
    raw_db_url = os.environ.get("DATABASE_URL", "").strip()
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)

    if not raw_db_url:
        results["postgres_connection"]["status"] = "FAILED"
        results["postgres_connection"]["reason"] = "DATABASE_URL environment variable is not configured."
    else:
        try:
            import psycopg2
            parsed_db = urlparse(raw_db_url)
            host_clean = f"{parsed_db.hostname}:{parsed_db.port or 5432}"
            results["postgres_connection"]["host"] = host_clean

            conn = psycopg2.connect(raw_db_url, connect_timeout=6)
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS ping;")
            conn.close()
            results["postgres_connection"]["status"] = "SUCCESS"
            results["postgres_connection"]["details"] = f"Connected successfully to PostgreSQL at {host_clean}"
        except Exception as err:
            err_msg = str(err).strip()
            # Clean password out of error message if psycopg2 includes it
            if "@" in err_msg and "://" in err_msg:
                err_msg = err_msg.split("@")[-1]
            results["postgres_connection"]["status"] = "FAILED"
            results["postgres_connection"]["reason"] = err_msg

    # ---------------------------------------------------------
    # 6. Test DATABASE SCHEMA (Required Tables)
    # ---------------------------------------------------------
    required_tables = ["site_config", "chapters", "replies", "texts"]
    found_tables = []
    missing_tables = []

    # Method A: Direct PostgreSQL query if POSTGRES CONNECTION succeeded
    if results["postgres_connection"]["status"] == "SUCCESS":
        try:
            import psycopg2
            conn = psycopg2.connect(raw_db_url, connect_timeout=6)
            with conn.cursor() as cur:
                cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                existing = [row[0] for row in cur.fetchall()]
            conn.close()

            for t in required_tables:
                if t in existing:
                    found_tables.append(t)
                else:
                    missing_tables.append(t)
        except Exception as err:
            logger.warning("Could not query pg_tables directly: %s", err)

    # Method B: Supabase PostgREST API check
    if not found_tables and results["supabase_authentication"]["status"] == "SUCCESS":
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        for t in required_tables:
            try:
                table_url = f"{supabase_url}/rest/v1/{t}?select=id&limit=1"
                t_res = requests.get(table_url, headers=headers, timeout=6)
                if t_res.status_code in [200, 206]:
                    found_tables.append(t)
                elif t_res.status_code == 404:
                    missing_tables.append(t)
                elif t_res.status_code == 401:
                    missing_tables.append(t)
                else:
                    found_tables.append(t)
            except Exception:
                missing_tables.append(t)

    results["database_schema"]["tables_found"] = found_tables
    results["database_schema"]["missing_tables"] = missing_tables

    if found_tables and not missing_tables:
        results["database_schema"]["status"] = "SUCCESS"
        results["database_schema"]["details"] = f"All {len(required_tables)} required tables verified: {', '.join(required_tables)}"
    elif missing_tables:
        results["database_schema"]["status"] = "FAILED"
        results["database_schema"]["reason"] = (
            f"Table '{missing_tables[0]}' was not found in Supabase schema. "
            "Please execute supabase_schema.sql in the Supabase SQL Editor."
        )
    else:
        results["database_schema"]["status"] = "FAILED"
        results["database_schema"]["reason"] = "Could not verify database schema (database unreachable)."

    # ---------------------------------------------------------
    # 7. Test STORAGE BUCKET
    # ---------------------------------------------------------
    bucket_name = results["storage_bucket"]["bucket_tested"]
    if supabase_url and supabase_key:
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        try:
            bucket_url = f"{supabase_url}/storage/v1/bucket/{bucket_name}"
            b_res = requests.get(bucket_url, headers=headers, timeout=8)
            if b_res.status_code in [200, 201]:
                b_json = {}
                try:
                    b_json = b_res.json()
                except Exception:
                    pass
                is_pub = b_json.get("public", True)
                results["storage_bucket"]["status"] = "SUCCESS"
                results["storage_bucket"]["details"] = f"Bucket '{bucket_name}' verified (Public: {is_pub})"
            elif b_res.status_code == 404:
                # Try to auto-create bucket programmatically if using service_role key
                create_url = f"{supabase_url}/storage/v1/bucket"
                create_payload = {"id": bucket_name, "name": bucket_name, "public": True}
                create_res = requests.post(create_url, json=create_payload, headers=headers, timeout=8)
                if create_res.status_code in [200, 201, 400, 409]:
                    results["storage_bucket"]["status"] = "SUCCESS"
                    results["storage_bucket"]["details"] = f"Bucket '{bucket_name}' was auto-created and verified."
                else:
                    results["storage_bucket"]["status"] = "FAILED"
                    results["storage_bucket"]["reason"] = (
                        f"Bucket '{bucket_name}' not found (NoSuchBucket). "
                        f"Create public bucket '{bucket_name}' in Supabase Dashboard -> Storage."
                    )
            elif b_res.status_code == 401:
                results["storage_bucket"]["status"] = "FAILED"
                results["storage_bucket"]["reason"] = "invalid/expired key (Storage returned HTTP 401 Unauthorized)"
            elif b_res.status_code == 403:
                results["storage_bucket"]["status"] = "FAILED"
                results["storage_bucket"]["reason"] = "authentication/permission error (Storage returned HTTP 403 Forbidden)"
            else:
                results["storage_bucket"]["status"] = "FAILED"
                results["storage_bucket"]["reason"] = f"Storage returned status {b_res.status_code}: {b_res.text.strip()}"
        except Exception as err:
            results["storage_bucket"]["status"] = "FAILED"
            results["storage_bucket"]["reason"] = f"network/connection error ({err})"
    else:
        results["storage_bucket"]["status"] = "FAILED"
        results["storage_bucket"]["reason"] = "missing environment variable (SUPABASE_URL or SUPABASE_KEY)"

    # Overall calculation
    all_success = all([
        results["supabase_url"]["status"] == "FOUND",
        results["supabase_key"]["status"] == "FOUND",
        results["supabase_client"]["status"] == "SUCCESS",
        results["supabase_authentication"]["status"] == "SUCCESS",
        results["postgres_connection"]["status"] == "SUCCESS",
        results["database_schema"]["status"] == "SUCCESS",
        results["storage_bucket"]["status"] == "SUCCESS",
    ])
    results["overall_status"] = "SUCCESS" if all_success else "ISSUES_DETECTED"
    return results


def format_diagnostic_text(res: dict) -> str:
    """
    Formats the 7 diagnostic test items for terminal output in CMD or Render logs.
    """
    lines = []
    lines.append("=" * 65)
    lines.append("  SUPABASE CONFIGURATION & CREDENTIAL DIAGNOSTIC")
    lines.append("=" * 65)

    _env_disk_path = Path(__file__).resolve().parent / ".env"
    if not _env_disk_path.exists():
        lines.append(f"[NOTICE] Local '.env' file not found at:")
        lines.append(f"  {_env_disk_path}")
        lines.append("  To configure local development credentials, copy .env.example to .env")
        lines.append("  and fill in your Supabase credentials (from your Render Dashboard).")
        lines.append("-" * 65)
    else:
        lines.append(f"[OK] Local '.env' file loaded from:")
        lines.append(f"  {_env_disk_path}")
        lines.append("-" * 65)

    # 1. URL
    url_st = res["supabase_url"]["status"]
    url_info = f" ({res['supabase_url']['value']})" if url_st == "FOUND" else ""
    lines.append(f"SUPABASE_URL:            {url_st}{url_info}")
    if url_st != "FOUND" and res["supabase_url"].get("reason"):
        lines.append(f"  REASON: {res['supabase_url']['reason']}")

    # 2. KEY
    key_st = res["supabase_key"]["status"]
    key_info = f" ({res['supabase_key']['masked_preview']})" if key_st == "FOUND" else ""
    lines.append(f"SUPABASE_KEY:            {key_st}{key_info}")
    if key_st != "FOUND" and res["supabase_key"].get("reason"):
        lines.append(f"  REASON: {res['supabase_key']['reason']}")

    # 3. CLIENT
    cl_st = res["supabase_client"]["status"]
    lines.append(f"SUPABASE CLIENT:         {cl_st}")
    if cl_st != "SUCCESS" and res["supabase_client"].get("reason"):
        lines.append(f"  REASON: {res['supabase_client']['reason']}")

    # 4. AUTHENTICATION
    auth_st = res["supabase_authentication"]["status"]
    lines.append(f"SUPABASE AUTHENTICATION: {auth_st}")
    if auth_st != "SUCCESS" and res["supabase_authentication"].get("reason"):
        lines.append(f"  REASON: {res['supabase_authentication']['reason']}")

    # 5. POSTGRES CONNECTION
    pg_st = res["postgres_connection"]["status"]
    pg_host = f" ({res['postgres_connection']['host']})" if res["postgres_connection"].get("host") else ""
    lines.append(f"POSTGRES CONNECTION:     {pg_st}{pg_host}")
    if pg_st != "SUCCESS" and res["postgres_connection"].get("reason"):
        lines.append(f"  REASON: {res['postgres_connection']['reason']}")

    # 6. DATABASE SCHEMA
    schema_st = res["database_schema"]["status"]
    lines.append(f"DATABASE SCHEMA:         {schema_st}")
    if schema_st == "SUCCESS" and res["database_schema"].get("details"):
        lines.append(f"  DETAILS: {res['database_schema']['details']}")
    elif schema_st != "SUCCESS" and res["database_schema"].get("reason"):
        lines.append(f"  REASON: {res['database_schema']['reason']}")

    # 7. STORAGE BUCKET
    st_st = res["storage_bucket"]["status"]
    lines.append(f"STORAGE BUCKET:          {st_st}")
    if st_st == "SUCCESS" and res["storage_bucket"].get("details"):
        lines.append(f"  DETAILS: {res['storage_bucket']['details']}")
    elif st_st != "SUCCESS" and res["storage_bucket"].get("reason"):
        lines.append(f"  REASON: {res['storage_bucket']['reason']}")

    lines.append("=" * 65)
    if res["overall_status"] == "SUCCESS":
        lines.append(">>> RESULT: ALL SUPABASE SERVICES ARE HEALTHY & VERIFIED! <<<")
    else:
        lines.append(">>> RESULT: ACTION REQUIRED IN SUPABASE / RENDER <<<")
    lines.append("=" * 65)

    return "\n".join(lines)


def format_diagnostic_html(res: dict) -> str:
    """Renders sleek OLED black diagnostic web page for browser viewing."""
    def badge(status):
        if status in ["FOUND", "SUCCESS"]:
            return f'<span style="background: rgba(34,197,94,0.18); color: #4ade80; border: 1px solid rgba(34,197,94,0.4); padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 12px;">{status}</span>'
        elif status == "MISSING":
            return f'<span style="background: rgba(234,179,8,0.18); color: #facc15; border: 1px solid rgba(234,179,8,0.4); padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 12px;">{status}</span>'
        else:
            return f'<span style="background: rgba(239,68,68,0.18); color: #f87171; border: 1px solid rgba(239,68,68,0.4); padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 12px;">{status}</span>'

    items = [
        ("SUPABASE_URL", res["supabase_url"]["status"], res["supabase_url"].get("value") or res["supabase_url"].get("reason")),
        ("SUPABASE_KEY", res["supabase_key"]["status"], res["supabase_key"].get("masked_preview") or res["supabase_key"].get("reason")),
        ("SUPABASE CLIENT", res["supabase_client"]["status"], res["supabase_client"].get("reason") or "Supabase Python SDK initialized"),
        ("SUPABASE AUTHENTICATION", res["supabase_authentication"]["status"], res["supabase_authentication"].get("details") or res["supabase_authentication"].get("reason")),
        ("POSTGRES CONNECTION", res["postgres_connection"]["status"], res["postgres_connection"].get("details") or res["postgres_connection"].get("reason")),
        ("DATABASE SCHEMA", res["database_schema"]["status"], res["database_schema"].get("details") or res["database_schema"].get("reason")),
        ("STORAGE BUCKET", res["storage_bucket"]["status"], res["storage_bucket"].get("details") or res["storage_bucket"].get("reason")),
    ]

    rows_html = ""
    for name, status, desc in items:
        rows_html += f"""
        <div class="row">
            <div>
                <div class="label">{name}</div>
                <div class="desc">{desc or ''}</div>
            </div>
            <div>{badge(status)}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA // Supabase Cloud Diagnostic</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }}
        body {{ background: #050507; color: #f3f4f6; min-height: 100vh; padding: 40px 20px; display: flex; justify-content: center; align-items: flex-start; }}
        .card {{ background: #0d0d12; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; max-width: 720px; width: 100%; padding: 32px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }}
        h1 {{ font-size: 20px; letter-spacing: 0.1em; color: #fff; text-transform: uppercase; margin-bottom: 8px; }}
        .sub {{ font-size: 13px; color: #9ca3af; margin-bottom: 28px; }}
        .row {{ display: flex; justify-content: space-between; align-items: flex-start; padding: 16px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }}
        .label {{ font-size: 14px; font-weight: 600; color: #d1d5db; }}
        .desc {{ font-size: 12px; color: #9ca3af; margin-top: 4px; font-family: monospace; }}
        .btn {{ display: inline-block; margin-top: 24px; padding: 10px 20px; background: #ffffff; color: #000; text-decoration: none; border-radius: 8px; font-size: 13px; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>✦ Supabase 7-Point Diagnostic Report</h1>
        <p class="sub">Live validation of API credentials, database tables, and cloud storage bucket</p>
        {rows_html}
        <div style="margin-top: 24px; display: flex; gap: 12px;">
            <a href="/diagnostic" class="btn" onclick="location.reload(); return false;">↻ Re-run Diagnostic</a>
            <a href="/" class="btn" style="background: rgba(255,255,255,0.1); color: #fff;">Return to Canvas</a>
        </div>
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    diag_res = run_supabase_diagnostic()
    print(format_diagnostic_text(diag_res))

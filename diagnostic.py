"""
Supabase Configuration & Credential Diagnostic Module
=====================================================
Performs non-destructive, read-only verification of Supabase API credentials:
1. Checks SUPABASE_URL presence and validity.
2. Checks SUPABASE_KEY presence (never prints or exposes secret keys).
3. Verifies Supabase Client creation.
4. Verifies network connectivity & authentication against Supabase REST API.
5. Performs a real read operation on project tables ('chapters', 'site_config', etc.).
6. Verifies Supabase Storage connectivity & bucket existence ('memories').
7. Distinguishes exact error causes:
   - missing environment variable
   - invalid URL
   - invalid/expired key
   - authentication/permission error
   - table does not exist
   - Storage bucket does not exist
   - network/connection error
   - successful connection.
"""

import os
import sys
import logging
from urllib.parse import urlparse
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger("aura.diagnostic")


def run_supabase_diagnostic() -> dict:
    """
    Executes a complete diagnostic test suite against the Supabase configuration.
    Guarantees no sensitive keys are leaked and no data is modified or deleted.
    """
    results = {
        "supabase_url": {
            "status": "UNKNOWN",
            "value": None,
            "reason": None
        },
        "supabase_key": {
            "status": "UNKNOWN",
            "exists": False,
            "masked_preview": None,
            "key_type": None,
            "reason": None
        },
        "supabase_client": {
            "status": "UNKNOWN",
            "reason": None
        },
        "database_connection": {
            "status": "UNKNOWN",
            "table_tested": None,
            "reason": None,
            "details": None
        },
        "storage_connection": {
            "status": "UNKNOWN",
            "bucket_tested": None,
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
        results["supabase_url"]["reason"] = "missing environment variable (SUPABASE_URL is not set)"
    else:
        parsed = urlparse(raw_url)
        if not parsed.scheme or not parsed.netloc:
            results["supabase_url"]["status"] = "INVALID"
            results["supabase_url"]["reason"] = f"invalid URL format ('{raw_url}')"
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
        results["supabase_key"]["exists"] = False
        results["supabase_key"]["reason"] = "missing environment variable (SUPABASE_KEY is not set)"
    else:
        results["supabase_key"]["status"] = "FOUND"
        results["supabase_key"]["exists"] = True
        key_type = "JWT Token" if raw_key.startswith("ey") else "API Key"
        # Strictly mask key for security (never display full key)
        if len(raw_key) > 12:
            masked = f"{raw_key[:4]}...{raw_key[-4:]} (Length: {len(raw_key)})"
        else:
            masked = f"[MASKED - Length: {len(raw_key)}]"
        results["supabase_key"]["masked_preview"] = masked
        results["supabase_key"]["key_type"] = key_type

    # If either URL or Key is missing, skip remaining network tests
    if results["supabase_url"]["status"] != "FOUND" or results["supabase_key"]["status"] != "FOUND":
        results["supabase_client"]["status"] = "SKIPPED"
        results["supabase_client"]["reason"] = "missing environment variable"
        results["database_connection"]["status"] = "SKIPPED"
        results["database_connection"]["reason"] = "missing environment variable"
        results["storage_connection"]["status"] = "SKIPPED"
        results["storage_connection"]["reason"] = "missing environment variable"
        results["overall_status"] = "CONFIG_MISSING"
        return results

    supabase_url = results["supabase_url"]["value"]
    supabase_key = raw_key
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }

    # ---------------------------------------------------------
    # 3. Test Supabase Client Creation
    # ---------------------------------------------------------
    try:
        import supabase
        _client = supabase.create_client(supabase_url, supabase_key)
        results["supabase_client"]["status"] = "CREATED"
    except Exception as err:
        results["supabase_client"]["status"] = "FAILED"
        results["supabase_client"]["reason"] = f"client initialization error ({err})"

    # ---------------------------------------------------------
    # 4 & 5. Test Database Connection & Real Read Operation
    # ---------------------------------------------------------
    test_tables = ["chapters", "site_config", "replies", "texts"]
    db_success = False
    table_tested = test_tables[0]
    results["database_connection"]["table_tested"] = table_tested

    try:
        test_url = f"{supabase_url}/rest/v1/{table_tested}?select=id&limit=1"
        res = requests.get(test_url, headers=headers, timeout=8)

        if res.status_code in [200, 206]:
            results["database_connection"]["status"] = "SUCCESS"
            results["database_connection"]["details"] = f"Read operation succeeded on table '{table_tested}' (HTTP {res.status_code})"
            db_success = True
        elif res.status_code == 401:
            results["database_connection"]["status"] = "FAILED"
            results["database_connection"]["reason"] = "invalid/expired key"
            results["database_connection"]["details"] = f"Supabase rejected API key (HTTP 401 Unauthorized: {res.text.strip()})"
        elif res.status_code == 403:
            results["database_connection"]["status"] = "FAILED"
            results["database_connection"]["reason"] = "authentication/permission error"
            results["database_connection"]["details"] = f"Row-level security or API key lacks read permission on table '{table_tested}' (HTTP 403 Forbidden)"
        elif res.status_code == 404:
            # Check if it's "table does not exist"
            err_text = res.text
            if "relation" in err_text or "PGRST205" in err_text or "not found" in err_text.lower():
                results["database_connection"]["status"] = "FAILED"
                results["database_connection"]["reason"] = "table does not exist"
                results["database_connection"]["details"] = f"Table '{table_tested}' was not found in Supabase schema. You must execute supabase_schema.sql in the Supabase SQL Editor."
            else:
                results["database_connection"]["status"] = "FAILED"
                results["database_connection"]["reason"] = "table does not exist"
                results["database_connection"]["details"] = f"Endpoint returned 404: {err_text}"
        else:
            results["database_connection"]["status"] = "FAILED"
            results["database_connection"]["reason"] = f"HTTP {res.status_code}"
            results["database_connection"]["details"] = res.text.strip()

    except requests.exceptions.ConnectionError as err:
        results["database_connection"]["status"] = "FAILED"
        results["database_connection"]["reason"] = "network/connection error"
        results["database_connection"]["details"] = f"Could not reach {supabase_url} ({err})"
    except requests.exceptions.Timeout:
        results["database_connection"]["status"] = "FAILED"
        results["database_connection"]["reason"] = "network/connection error"
        results["database_connection"]["details"] = "Connection to Supabase REST API timed out after 8 seconds."
    except Exception as err:
        results["database_connection"]["status"] = "FAILED"
        results["database_connection"]["reason"] = "network/connection error"
        results["database_connection"]["details"] = str(err)

    # ---------------------------------------------------------
    # 6. Test Supabase Storage Connectivity & Bucket Check
    # ---------------------------------------------------------
    bucket_name = os.environ.get("SUPABASE_BUCKET", "memories").strip()
    results["storage_connection"]["bucket_tested"] = bucket_name

    try:
        bucket_url = f"{supabase_url}/storage/v1/bucket/{bucket_name}"
        res = requests.get(bucket_url, headers=headers, timeout=8)

        if res.status_code in [200, 201]:
            b_info = {}
            try:
                b_info = res.json()
            except Exception:
                pass
            is_public = b_info.get("public", True)
            results["storage_connection"]["status"] = "SUCCESS"
            results["storage_connection"]["details"] = f"Bucket '{bucket_name}' verified (Public: {is_public})"
        elif res.status_code == 404:
            # Check if storage is reachable at all by listing buckets
            list_url = f"{supabase_url}/storage/v1/bucket"
            list_res = requests.get(list_url, headers=headers, timeout=8)
            if list_res.status_code == 401:
                results["storage_connection"]["status"] = "FAILED"
                results["storage_connection"]["reason"] = "invalid/expired key"
                results["storage_connection"]["details"] = "Storage service rejected API key (HTTP 401 Unauthorized)"
            elif list_res.status_code == 403:
                results["storage_connection"]["status"] = "FAILED"
                results["storage_connection"]["reason"] = "authentication/permission error"
                results["storage_connection"]["details"] = "Storage service denied access (HTTP 403 Forbidden)"
            else:
                results["storage_connection"]["status"] = "FAILED"
                results["storage_connection"]["reason"] = "Storage bucket does not exist"
                results["storage_connection"]["details"] = (
                    f"Bucket '{bucket_name}' not found in Supabase Storage. "
                    f"Please create the bucket '{bucket_name}' in your Supabase Dashboard -> Storage."
                )
        elif res.status_code == 401:
            results["storage_connection"]["status"] = "FAILED"
            results["storage_connection"]["reason"] = "invalid/expired key"
            results["storage_connection"]["details"] = "Storage endpoint returned HTTP 401 Unauthorized"
        elif res.status_code == 403:
            results["storage_connection"]["status"] = "FAILED"
            results["storage_connection"]["reason"] = "authentication/permission error"
            results["storage_connection"]["details"] = "Storage endpoint returned HTTP 403 Forbidden"
        else:
            results["storage_connection"]["status"] = "FAILED"
            results["storage_connection"]["reason"] = f"HTTP {res.status_code}"
            results["storage_connection"]["details"] = res.text.strip()

    except requests.exceptions.ConnectionError as err:
        results["storage_connection"]["status"] = "FAILED"
        results["storage_connection"]["reason"] = "network/connection error"
        results["storage_connection"]["details"] = f"Could not connect to Storage endpoint at {supabase_url} ({err})"
    except requests.exceptions.Timeout:
        results["storage_connection"]["status"] = "FAILED"
        results["storage_connection"]["reason"] = "network/connection error"
        results["storage_connection"]["details"] = "Storage endpoint connection timed out."
    except Exception as err:
        results["storage_connection"]["status"] = "FAILED"
        results["storage_connection"]["reason"] = "network/connection error"
        results["storage_connection"]["details"] = str(err)

    # ---------------------------------------------------------
    # Overall Status Calculation
    # ---------------------------------------------------------
    if (results["database_connection"]["status"] == "SUCCESS"
            and results["storage_connection"]["status"] == "SUCCESS"):
        results["overall_status"] = "SUCCESS"
    else:
        results["overall_status"] = "ISSUES_DETECTED"

    return results


def format_diagnostic_text(res: dict) -> str:
    """
    Formats the diagnostic results for clean console output in CMD.
    Produces the exact format requested:
      SUPABASE_URL: FOUND
      SUPABASE_KEY: FOUND
      SUPABASE CLIENT: CREATED
      DATABASE CONNECTION: SUCCESS
      STORAGE CONNECTION: SUCCESS
    or displays clear failure reasons.
    """
    lines = []
    lines.append("=" * 65)
    lines.append("  SUPABASE CONFIGURATION & CREDENTIAL DIAGNOSTIC")
    lines.append("=" * 65)

    # 1. URL
    url_st = res["supabase_url"]["status"]
    lines.append(f"SUPABASE_URL: {url_st}")
    if url_st == "FOUND":
        lines.append(f"  Endpoint: {res['supabase_url']['value']}")
    elif res["supabase_url"].get("reason"):
        lines.append(f"  REASON: {res['supabase_url']['reason']}")

    # 2. Key
    key_st = res["supabase_key"]["status"]
    lines.append(f"SUPABASE_KEY: {key_st}")
    if key_st == "FOUND":
        lines.append(f"  Key Info: {res['supabase_key']['masked_preview']} ({res['supabase_key']['key_type']})")
    elif res["supabase_key"].get("reason"):
        lines.append(f"  REASON: {res['supabase_key']['reason']}")

    # 3. Client
    client_st = res["supabase_client"]["status"]
    lines.append(f"SUPABASE CLIENT: {client_st}")
    if client_st not in ["CREATED", "UNKNOWN"] and res["supabase_client"].get("reason"):
        lines.append(f"  REASON: {res['supabase_client']['reason']}")

    # 4. Database
    db_st = res["database_connection"]["status"]
    lines.append(f"DATABASE CONNECTION: {db_st}")
    if db_st == "SUCCESS":
        lines.append(f"  {res['database_connection']['details']}")
    else:
        if res["database_connection"].get("reason"):
            lines.append(f"  REASON: {res['database_connection']['reason']}")
        if res["database_connection"].get("details"):
            lines.append(f"  DETAILS: {res['database_connection']['details']}")

    # 5. Storage
    st_st = res["storage_connection"]["status"]
    lines.append(f"STORAGE CONNECTION: {st_st}")
    if st_st == "SUCCESS":
        lines.append(f"  {res['storage_connection']['details']}")
    else:
        if res["storage_connection"].get("reason"):
            lines.append(f"  REASON: {res['storage_connection']['reason']}")
        if res["storage_connection"].get("details"):
            lines.append(f"  DETAILS: {res['storage_connection']['details']}")

    lines.append("=" * 65)

    if res["overall_status"] == "SUCCESS":
        lines.append(">>> RESULT: ALL SUPABASE API CREDENTIALS ARE VALID & VERIFIED! <<<")
    else:
        lines.append(">>> RESULT: CONFIGURATION OR PERMISSION ISSUES DETECTED. <<<")
    lines.append("=" * 65)

    return "\n".join(lines)


def format_diagnostic_html(res: dict) -> str:
    """Renders a sleek OLED black diagnostic web page for browser viewing."""
    def badge(status):
        if status in ["FOUND", "CREATED", "SUCCESS"]:
            return f'<span style="background: rgba(34,197,94,0.18); color: #4ade80; border: 1px solid rgba(34,197,94,0.4); padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 12px; letter-spacing: 0.05em;">{status}</span>'
        elif status == "MISSING":
            return f'<span style="background: rgba(234,179,8,0.18); color: #facc15; border: 1px solid rgba(234,179,8,0.4); padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 12px; letter-spacing: 0.05em;">{status}</span>'
        else:
            return f'<span style="background: rgba(239,68,68,0.18); color: #f87171; border: 1px solid rgba(239,68,68,0.4); padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 12px; letter-spacing: 0.05em;">{status}</span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA // Supabase Configuration Diagnostic</title>
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
        .btn:hover {{ background: #e5e7eb; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>✦ Supabase Diagnostic Report</h1>
        <p class="sub">Read-only live validation of project API credentials & cloud reachability</p>

        <div class="row">
            <div>
                <div class="label">SUPABASE_URL</div>
                <div class="desc">{res["supabase_url"].get("value") or res["supabase_url"].get("reason")}</div>
            </div>
            <div>{badge(res["supabase_url"]["status"])}</div>
        </div>

        <div class="row">
            <div>
                <div class="label">SUPABASE_KEY</div>
                <div class="desc">{res["supabase_key"].get("masked_preview") or res["supabase_key"].get("reason")}</div>
            </div>
            <div>{badge(res["supabase_key"]["status"])}</div>
        </div>

        <div class="row">
            <div>
                <div class="label">SUPABASE CLIENT</div>
                <div class="desc">{res["supabase_client"].get("reason") or "Supabase Python Client initialization"}</div>
            </div>
            <div>{badge(res["supabase_client"]["status"])}</div>
        </div>

        <div class="row">
            <div>
                <div class="label">DATABASE CONNECTION</div>
                <div class="desc">
                    Tested table: <strong>{res["database_connection"].get("table_tested") or "None"}</strong><br>
                    {res["database_connection"].get("reason") and f'<span style="color:#f87171;">REASON: {res["database_connection"].get("reason")}</span><br>' or ''}
                    {res["database_connection"].get("details") or ''}
                </div>
            </div>
            <div>{badge(res["database_connection"]["status"])}</div>
        </div>

        <div class="row">
            <div>
                <div class="label">STORAGE CONNECTION</div>
                <div class="desc">
                    Tested bucket: <strong>{res["storage_connection"].get("bucket_tested") or "None"}</strong><br>
                    {res["storage_connection"].get("reason") and f'<span style="color:#f87171;">REASON: {res["storage_connection"].get("reason")}</span><br>' or ''}
                    {res["storage_connection"].get("details") or ''}
                </div>
            </div>
            <div>{badge(res["storage_connection"]["status"])}</div>
        </div>

        <div style="margin-top: 24px; display: flex; gap: 12px;">
            <a href="/diagnostic" class="btn" onclick="location.reload(); return false;">↻ Re-run Diagnostic</a>
            <a href="/" class="btn" style="background: rgba(255,255,255,0.1); color: #fff;">Return to Canvas</a>
        </div>
    </div>
</body>
</html>
"""
    return html


if __name__ == "__main__":
    diag_res = run_supabase_diagnostic()
    print(format_diagnostic_text(diag_res))

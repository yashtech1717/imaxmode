"""
Standalone CLI Supabase Credential Verification Tool
===================================================
Run this directly in CMD:
    python verify_supabase.py

Tests:
1. SUPABASE_URL existence & syntax
2. SUPABASE_KEY existence (masked, never leaked)
3. Supabase Python Client creation
4. Network connectivity to Supabase REST API
5. Real read operation on project tables ('chapters', 'site_config', etc.)
6. Supabase Storage bucket connectivity ('memories')
"""

import sys
import os

# Ensure current directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diagnostic import run_supabase_diagnostic, format_diagnostic_text

def main():
    results = run_supabase_diagnostic()
    print(format_diagnostic_text(results))
    if results.get("overall_status") == "SUCCESS":
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

import os, sqlite3, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_audit():
    print("\n   [+] Running Sovereign Core v1.5.0-beta Security & SQLite v7 Audit...")
    assert ".venv" in sys.executable, "CRITICAL: Not running inside .venv sandbox!"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA user_version;")
    ver = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM global_assets_v7")
    asset_count = cursor.fetchone()[0]
    conn.close()
    
    assert ver >= 7, "SQLite schema version v7 check failed!"
    assert asset_count >= 40, f"Missing top-tier assets! Only found {asset_count}"
    print(f"   [PASS] Schema v{ver} verified. {asset_count} Global Assets tracked securely.")
    print("   [PASS] ALL SYSTEM AUDIT TESTS PASSED SUCCESSFULLY.\n")

if __name__ == "__main__":
    run_audit()

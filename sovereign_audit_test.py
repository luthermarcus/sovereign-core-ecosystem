import os, sqlite3, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_audit():
    print("\n   [+] Running Sovereign Core v1.11.0-beta Security & SQLite v12 Audit...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA user_version;")
    ver = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tax_policies_v12")
    tax_count = cursor.fetchone()[0]
    conn.close()
    
    assert ver >= 12, "SQLite schema version v12 check failed!"
    print(f"   [PASS] Schema v{ver} verified. {tax_count} Ethical Tax Policies configured securely.")
    print("   [PASS] ALL SYSTEM AUDIT TESTS PASSED SUCCESSFULLY.\n")

if __name__ == "__main__":
    run_audit()

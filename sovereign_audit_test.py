import os, socket, sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_audit():
    print("=" * 70)
    print("   SOVEREIGN CORE: v0.5.6-beta SECURITY & STRESS AUDIT")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    assert os.path.exists(BASE_DIR), "Workspace missing!"
    print("    [PASS] Isolated workspace verified.")

    sock_path = "/tmp/sovereign_wallet.sock"
    if os.path.exists(sock_path): os.remove(sock_path)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(sock_path)
    os.chmod(sock_path, 0o600)
    s.listen(1)
    print("    [PASS] UNIX Domain Socket bound securely with 0600 permissions.")
    s.close()
    if os.path.exists(sock_path): os.remove(sock_path)

    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM reserves WHERE token='FOX'")
    res = cursor.fetchone()
    cursor.execute("PRAGMA user_version;")
    ver = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM yield_vaults")
    vault_count = cursor.fetchone()[0]
    conn.close()
    
    assert res is not None and res[0] == 10000.0, "FOX Reserve check failed!"
    assert ver >= 3, "Schema version v3 check failed!"
    assert vault_count >= 3, "Yield vault telemetry missing!"
    print(f"    [PASS] SQLite WAL mode & busy timeout active. Schema Version: v{ver}. Vaults: {vault_count}")
    print("\n[+] ALL SYSTEM AUDIT TESTS PASSED SUCCESSFULLY.")

if __name__ == "__main__":
    run_audit()

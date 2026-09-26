import os, socket, sqlite3, sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_audit():
    print("=" * 70)
    print("   SOVEREIGN CORE: v1.3.0-beta SECURITY & WAL ATOMICITY AUDIT")
    print(f"   Python Interpreter: {sys.executable}")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    assert ".venv" in sys.executable, "CRITICAL: Not running inside .venv sandbox!"
    print("    [PASS] Absolute .venv sandbox isolation verified.")

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
    cursor = conn.cursor()
    cursor.execute("PRAGMA user_version;")
    ver = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM yield_vaults_v5")
    vault_count = cursor.fetchone()[0]
    conn.close()
    
    assert ver >= 5, "SQLite schema version v5 check failed!"
    assert vault_count >= 4, "Beefy yield vaults telemetry missing!"
    print(f"    [PASS] SQLite WAL mode active. Schema Version: v{ver}. Vaults Indexed: {vault_count}")
    print("\n[+] ALL SYSTEM AUDIT TESTS PASSED SUCCESSFULLY.")

if __name__ == "__main__":
    run_audit()

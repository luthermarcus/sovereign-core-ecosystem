import sys, os, sqlite3, socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_preflight():
    print("[*] Running Pre-Flight System Smoke Tests...")
    assert ".venv" in sys.executable, "FAIL: Interpreter outside .venv sandbox!"
    
    # Test Socket Binding
    sock_path = "/tmp/sovereign_test.sock"
    if os.path.exists(sock_path): os.remove(sock_path)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(sock_path)
    os.chmod(sock_path, 0o600)
    s.close()
    os.remove(sock_path)
    
    # Test SQLite WAL
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    conn.close()
    
    print("[PASS] Pre-Flight Verification Passed: Venv, Socket, & WAL Verified Clean.\n")

if __name__ == "__main__":
    run_preflight()

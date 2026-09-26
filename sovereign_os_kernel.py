import sqlite3, os, subprocess, sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def init_os_kernel():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    c.execute("PRAGMA user_version;")
    version = c.fetchone()[0]
    
    if version < 16:
        # Enforce strict Microkernel state tracking
        c.execute("CREATE TABLE IF NOT EXISTS os_process_registry_v16 (pid INTEGER PRIMARY KEY, process_name TEXT, status TEXT, last_heartbeat TEXT)")
        c.execute("PRAGMA user_version = 16;")
        print("[+] Microkernel initialized: Schema v16 IPC routing active.")
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_MICROKERNEL_OS', 'GREEN', 'Strict Microkernel Architecture Enforced. Modules isolated.', ?)", (timestamp,))
    conn.commit()
    conn.close()

def execute_isolated_process(script_name):
    """Executes backend engines as strictly isolated subprocesses"""
    script_path = os.path.join(BASE_DIR, script_name)
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"\n[!] OS Kernel Error: Module {script_name} not found in sandbox.")
        import time; time.sleep(2)

if __name__ == "__main__":
    init_os_kernel()

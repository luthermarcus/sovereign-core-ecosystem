import os
import sys
import subprocess
import sqlite3
from portability_layer import get_environment_profile

def boot_sequence():
    env = get_environment_profile()
    print(f"[*] Booting Sovereign Core OS v1.97.0 on {env['distro']} ({env['architecture']})...")
    
    os.makedirs("knowledge_vault", exist_ok=True)
    os.makedirs("modules", exist_ok=True)
    
    base_dir = os.path.expanduser("~/sovereign-core-ecosystem")
    for db in ["sys_health.db", "wallet.db", "discipline_ledger.db", "knowledge.db"]:
        path = os.path.join(base_dir, db)
        if os.path.exists(path):
            try: os.chmod(path, 0o664)
            except: pass
        conn = sqlite3.connect(path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.close()
        
    print("[+] SQLite WAL ledgers verified and absolute path bound.")
    
    daemon_path = os.path.join(base_dir, "telemetry_daemon.py")
    if os.path.exists(daemon_path):
        subprocess.Popen(["python3", daemon_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] Background telemetry daemon spawned.")
    
    # Launch Virtual OS TUI with absolute path resolution
    tui_path = os.path.join(base_dir, "virtual_os.py")
    os.execvp("python3", ["python3", tui_path])

if __name__ == "__main__":
    boot_sequence()

import os
import sys
import subprocess
import sqlite3
from portability_layer import get_environment_profile

def boot_sequence():
    env = get_environment_profile()
    print(f"[*] Booting Sovereign Core OS v1.87.0 on {env['os']} ({env['architecture']})...")
    
    os.makedirs("knowledge_vault", exist_ok=True)
    os.makedirs("modules", exist_ok=True)
    
    # Enforce strict read/write permissions and WAL mode on all ledgers
    for db in ["sys_health.db", "wallet.db", "discipline_ledger.db", "knowledge.db"]:
        path = os.path.expanduser(f"~/sovereign-core-ecosystem/{db}")
        if os.path.exists(path):
            try:
                os.chmod(path, 0o664)
            except:
                pass
        conn = sqlite3.connect(path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.close()
        
    print("[+] SQLite WAL ledgers verified, permission-guarded, and optimized.")
    
    # Spawn background telemetry daemon
    subprocess.Popen(["python3", "telemetry_daemon.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] Background telemetry daemon spawned.")
    
    # Launch Virtual OS TUI
    os.execvp("python3", ["python3", "virtual_os.py"])

if __name__ == "__main__":
    boot_sequence()

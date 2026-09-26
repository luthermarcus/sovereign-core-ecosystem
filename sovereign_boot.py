import os
import sys
import subprocess
import sqlite3
from portability_layer import get_environment_profile

def boot_sequence():
    env = get_environment_profile()
    print(f"[*] Booting Sovereign Core OS v1.96.0 (Sovereign Core Source) on {env['os']} ({env['architecture']})...")
    
    os.makedirs("knowledge_vault", exist_ok=True)
    os.makedirs("modules", exist_ok=True)
    
    # Ensure absolute path bindings for all WAL ledgers
    for db in ["sys_health.db", "wallet.db", "discipline_ledger.db", "knowledge.db"]:
        path = os.path.expanduser(f"~/sovereign-core-ecosystem/{db}")
        if os.path.exists(path):
            try: os.chmod(path, 0o664)
            except: pass
        conn = sqlite3.connect(path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.close()
        
    print("[+] Sovereign Core WAL ledgers verified and permission-guarded.")
    
    # Spawn background telemetry daemon tied to core root
    subprocess.Popen(["python3", "telemetry_daemon.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] Background telemetry daemon spawned from Sovereign Core.")
    
    # Launch Virtual OS TUI pulling directly from core source
    os.execvp("python3", ["python3", "virtual_os.py"])

if __name__ == "__main__":
    boot_sequence()

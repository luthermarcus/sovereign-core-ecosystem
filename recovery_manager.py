import os
import shutil
import datetime
import subprocess

# Sovereign Core Defense & Recovery Protocols
BACKUP_DIR = "/home/luther/node-stack/backups"
DB_LIST = ["sys_health.db", "node_history.db", "ecosystem_metrics.db"]

def execute_sqlite_backup():
    """Perform pre-execution copies of WAL databases to prevent corruption."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for db in DB_LIST:
        db_path = f"/home/luther/sovereign-core-ecosystem/{db}"
        if os.path.exists(db_path):
            shutil.copy2(db_path, f"{BACKUP_DIR}/{db}_{timestamp}.bak")
    print(f"[+] SQLite databases backed up to {BACKUP_DIR}")

def trigger_timeshift_snapshot():
    """Trigger system-level Timeshift snapshot for OS rollback."""
    try:
        # Requires sudo access; typically runs via automated root crontab
        subprocess.run(["sudo", "timeshift", "--create", "--comments", "Sovereign Core Auto-Backup"], check=True)
        print("[+] Timeshift system snapshot triggered.")
    except Exception:
        print("[-] Timeshift trigger failed or requires elevated privileges.")

def send_telegram_alert(message):
    """Push critical ecosystem alerts to mobile."""
    # Telegram Bot API integration hook
    pass 

if __name__ == "__main__":
    execute_sqlite_backup()

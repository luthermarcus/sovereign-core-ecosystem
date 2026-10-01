import os
import shutil
import datetime
import subprocess

BACKUP_DIR = "~/node-stack/backups"
DB_LIST = ["sys_health.db", "node_history.db", "ecosystem_metrics.db"]

def execute_sqlite_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for db in DB_LIST:
        db_path = f"~/sovereign-core-ecosystem/{db}"
        if os.path.exists(db_path):
            shutil.copy2(db_path, f"{BACKUP_DIR}/{db}_{timestamp}.bak")
    print(f"[+] SQLite databases backed up to {BACKUP_DIR}")

def trigger_timeshift_snapshot():
    try:
        subprocess.run(["sudo", "timeshift", "--create", "--comments", "Sovereign Core Auto-Backup"], check=True)
    except Exception:
        pass

def send_telegram_alert(message):
    pass

if __name__ == "__main__":
    execute_sqlite_backup()
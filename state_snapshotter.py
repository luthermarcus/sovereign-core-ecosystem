import tarfile
import os
import datetime

def snapshot_ram_state():
    print("[*] Initializing RAM WAL state snapshot sweep...")
    backup_dir = "/dev/shm/sovereign_backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(backup_dir, f"sovereign_state_{timestamp}.tar.gz")
    
    dbs = [
        "/dev/shm/sys_health.db",
        "/dev/shm/ecosystem_metrics.db",
        "/dev/shm/trust_store.db"
    ]
    
    with tarfile.open(archive_path, "w:gz") as tar:
        for db in dbs:
            if os.path.exists(db):
                tar.add(db, arcname=os.path.basename(db))
                
    print(f"[✓] RAM state successfully archived: {archive_path}")

if __name__ == "__main__":
    snapshot_ram_state()

import tarfile
import os
import sqlite3
import datetime

def snapshot_enclave():
    print("[*] Executing Sovereign Core RAM enclave snapshot sweep...")
    backup_dir = '/dev/shm/sovereign_backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(backup_dir, f"sovereign_enclave_snapshot_{timestamp}.tar.gz")
    
    databases = [
        "/dev/shm/ecosystem_metrics.db",
        "/dev/shm/sys_health.db",
        "/dev/shm/trust_store.db",
        "/dev/shm/ipc_bus.db"
    ]
    
    with tarfile.open(archive_path, "w:gz") as tar:
        for db in databases:
            if os.path.exists(db):
                tar.add(db, arcname=os.path.basename(db))
                
    db_path = '/dev/shm/ecosystem_metrics.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS snapshot_audit_logs (
                snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                archive_name TEXT,
                status TEXT,
                snapshotted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            INSERT INTO snapshot_audit_logs (archive_name, status)
            VALUES (?, ?)
        ''', (os.path.basename(archive_path), "SUCCESS_RAM_SECURE"))
        conn.commit()
        conn.close()
        
    print(f"[✓] RAM enclave successfully archived to: {archive_path}")

if __name__ == "__main__":
    snapshot_enclave()

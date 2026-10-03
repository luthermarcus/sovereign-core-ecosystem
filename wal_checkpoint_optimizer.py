import sqlite3
import os

def optimize_wal():
    print("[*] Executing RAM WAL checkpoint and vacuum optimizer sweep...")
    dbs = [
        "/dev/shm/sys_health.db",
        "/dev/shm/ecosystem_metrics.db",
        "/dev/shm/trust_store.db"
    ]
    
    for db in dbs:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
            conn.close()
            print(f"[✓] Checkpointed WAL for: {os.path.basename(db)}")
    print("[✓] RAM WAL optimization complete.")

if __name__ == "__main__":
    optimize_wal()

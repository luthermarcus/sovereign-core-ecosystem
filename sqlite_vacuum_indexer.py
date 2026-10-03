import sqlite3
import os

def optimize_sqlite_storage():
    print("[*] Executing Sovereign Core SQLite vacuum and fragmentation index sweep...")
    dbs = [
        "/dev/shm/ecosystem_metrics.db",
        "/dev/shm/sys_health.db",
        "/dev/shm/trust_store.db",
        "/dev/shm/ipc_bus.db"
    ]
    
    for db in dbs:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            conn.execute("VACUUM;")
            conn.execute("REINDEX;")
            conn.close()
            print(f"[✓] Defragmented and indexed RAM database: {os.path.basename(db)}")
    print("[✓] SQLite storage fragmentation optimization complete in RAM WAL.")

if __name__ == "__main__":
    optimize_sqlite_storage()

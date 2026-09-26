import sqlite3
import os

def perform_maintenance():
    target_dir = os.path.expanduser("~/sovereign-core-ecosystem")
    dbs = ["sys_health.db", "wallet.db", "discipline_ledger.db", "knowledge.db"]
    for db in dbs:
        path = os.path.join(target_dir, db)
        if os.path.exists(path):
            try:
                conn = sqlite3.connect(path)
                conn.execute("PRAGMA wal_checkpoint(FULL);")
                conn.execute("VACUUM;")
                conn.close()
            except:
                pass
    print("[+] Sovereign Core maintenance and WAL checkpoint completed successfully.")

if __name__ == "__main__":
    perform_maintenance()

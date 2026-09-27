import os, sys, time, sqlite3
sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class WALMaintenanceDaemon:
    DATABASES = [
        os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db"),
        os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db"),
        os.path.expanduser("~/sovereign-core-ecosystem/myst_metrics.db")
    ]

    @classmethod
    def execute_maintenance(cls):
        print("\n[*] [WAL MAINTENANCE] Initiating database checkpoint and telemetry archiving...")
        time.sleep(0.2)
        
        for db_path in cls.DATABASES:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                conn.close()
                print(f"[v] [WAL MAINTENANCE] Checkpoint truncated for: {os.path.basename(db_path)}")
                
        print("[v] [WAL MAINTENANCE] All storage ledgers optimized for low-latency persistence.")

if __name__ == "__main__":
    WALMaintenanceDaemon.execute_maintenance()

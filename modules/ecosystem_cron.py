import os, time, sqlite3, json
from modules.display_manager import MultiDisplayManager

class EcosystemTelemetryCron:
    DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")

    @classmethod
    def initialize_db(cls):
        conn = sqlite3.connect(cls.DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                gross_yield REAL,
                pol_tax REAL,
                thermal_c REAL,
                shm_mb REAL,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()

    @classmethod
    def record_snapshot(cls):
        cls.initialize_db()
        summary = MultiDisplayManager.render_all_displays_summary()
        d1 = summary["display_1_depin"]
        d2 = summary["display_2_hardware"]
        
        conn = sqlite3.connect(cls.DB_PATH)
        conn.execute(
            "INSERT INTO telemetry_logs (timestamp, gross_yield, pol_tax, thermal_c, shm_mb, status) VALUES (?, ?, ?, ?, ?, ?)",
            (time.time(), d1["gross"], d1["pol_tax"], d2["thermal_c"], d2["shm_mb"], "RECORDED")
        )
        conn.commit()
        conn.close()
        print(f"[v] Telemetry snapshot logged at {time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    EcosystemTelemetryCron.record_snapshot()

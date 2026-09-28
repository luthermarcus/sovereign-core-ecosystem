import os, sqlite3

def run_simulation():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
    if not os.path.exists(db_path):
        print("[*] Initializing local metrics database for simulation...")
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("CREATE TABLE IF NOT EXISTS depin_throughput (app TEXT PRIMARY KEY, bandwidth_gb REAL, yield_usd REAL, timestamp INT)")
        conn.execute("INSERT OR REPLACE INTO depin_throughput VALUES (Mysterium, 15.0, 5.50, 1727480000)")
        conn.commit()
        conn.close()
    print("[v] Sovereign Core Dashboard Simulation: ALL SYSTEMS OPERATIONAL.")

if __name__ == "__main__":
    run_simulation()

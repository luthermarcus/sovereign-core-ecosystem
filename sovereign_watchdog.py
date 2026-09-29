import os, sqlite3, time, subprocess

DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")

def verify_and_heal():
    """Validates SQLite metrics health and restarts dashboard if down."""
    print("[*] Watchdog pulse check initiated...")
    if not os.path.exists(DB_PATH):
        print("[!] Metrics DB missing. Initializing fresh WAL ledger...")
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("CREATE TABLE IF NOT EXISTS anomaly_ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, error TEXT, timestamp INTEGER)")
        conn.execute("CREATE TABLE IF NOT EXISTS depin_throughput (id INTEGER PRIMARY KEY AUTOINCREMENT, app TEXT, bandwidth_gb REAL, yield_usd REAL, timestamp INTEGER)")
        conn.commit()
        conn.close()
    
    # Check if dashboard service is running via systemctl
    res = subprocess.run(["systemctl", "--user", "is-active", "--quiet", "sovereign-dashboard.service"])
    if res.returncode != 0:
        print("[!] Dashboard service offline. Restarting...")
        subprocess.run(["systemctl", "--user", "restart", "sovereign-dashboard.service"])

if __name__ == "__main__":
    verify_and_heal()
    print("[v] Watchdog verification cycle complete.")

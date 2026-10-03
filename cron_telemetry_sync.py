import sqlite3
import json
import os

def sync_telemetry():
    print("[*] Running automated cron telemetry sync...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database not found.")
        return
    
    conn = sqlite3.connect(db_path)
    pools = conn.execute("SELECT pool_id, asset_symbol, total_staked FROM pool_allocations").fetchall()
    earnings = conn.execute("SELECT node_name, daily_yield, total_accumulated FROM depin_earnings").fetchall()
    conn.close()
    
    snapshot = {
        "pools": [{"pool": p[0], "asset": p[1], "staked": p[2]} for p in pools],
        "earnings": [{"node": e[0], "daily": e[1], "total": e[2]} for e in earnings]
    }
    
    with open("/dev/shm/telemetry_snapshot.json", "w") as f:
        json.dump(snapshot, f, indent=2)
    print("[✓] Telemetry snapshot synchronized in RAM.")

if __name__ == "__main__":
    sync_telemetry()

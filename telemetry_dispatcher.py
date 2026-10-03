import sqlite3
import os
import json

def dispatch_telemetry():
    print("[*] Executing Sovereign Core telemetry dispatch sweep...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database offline.")
        return
        
    conn = sqlite3.connect(db_path)
    pools = conn.execute("SELECT pool_id, total_staked FROM pool_allocations").fetchall()
    earnings = conn.execute("SELECT node_name, daily_yield FROM depin_earnings").fetchall()
    conn.close()
    
    summary = {
        "pools": {p[0]: p[1] for p in pools},
        "earnings": {e[0]: e[1] for e in earnings}
    }
    
    with open("/dev/shm/telemetry_dispatch.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("[✓] Telemetry dispatch payload prepared in RAM.")

if __name__ == "__main__":
    dispatch_telemetry()

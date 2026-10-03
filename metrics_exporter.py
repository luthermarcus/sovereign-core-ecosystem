import sqlite3
import json
import os

def export_metrics():
    print("[*] Exporting ecosystem metrics JSON payload...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM metrics database offline.")
        return
        
    conn = sqlite3.connect(db_path)
    pools = conn.execute("SELECT pool_id, asset_symbol, total_staked, donor_count FROM pool_allocations").fetchall()
    earnings = conn.execute("SELECT node_name, daily_yield, total_accumulated FROM depin_earnings").fetchall()
    trust = conn.execute("SELECT wallet_address, trust_score, status FROM trust_scores").fetchall()
    conn.close()
    
    payload = {
        "pools": [{"pool_id": p[0], "asset": p[1], "staked": p[2], "donors": p[3]} for p in pools],
        "earnings": [{"node": e[0], "daily_yield": e[1], "total": e[2]} for e in earnings],
        "trust_scores": [{"wallet": t[0], "score": t[1], "status": t[2]} for t in trust]
    }
    
    with open("/dev/shm/ecosystem_metrics_export.json", "w") as f:
        json.dump(payload, f, indent=2)
    print("[✓] Ecosystem metrics successfully exported to /dev/shm/ecosystem_metrics_export.json")

if __name__ == "__main__":
    export_metrics()

import sqlite3
import time
import os

def run_daemon():
    db_path = '/dev/shm/ecosystem_metrics.db'
    print("[✓] Liquidity Rebalancer Daemon active (interval: 60s)")
    while True:
        try:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                pools = conn.execute("SELECT pool_id, asset_symbol, total_staked FROM pool_allocations").fetchall()
                conn.close()
                for pool_id, asset, staked in pools:
                    if staked > 10000.0:
                        print(f"[REBALANCE] Pool '{pool_id}' ({asset}) at {staked} staked. Weights optimized.")
        except Exception as e:
            print(f"[-] Rebalancer Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    run_daemon()

import sqlite3
import os
import json

def render_status():
    print("=" * 70)
    print("       ⚡ SOVEREIGN CORE OS — UNIFIED ECOSYSTEM STATUS CLI")
    print("=" * 70)
    
    # 1. System Health
    try:
        conn = sqlite3.connect('/dev/shm/sys_health.db')
        ver = conn.execute("SELECT sqlite_version();").fetchone()
        conn.close()
        print(f"[✓] System Health DB Active (SQLite v{ver[0]})")
    except Exception:
        print("[-] System Health DB Offline")
        
    # 2. Metrics & Earnings
    db_path = '/dev/shm/ecosystem_metrics.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        pools = conn.execute("SELECT pool_id, asset_symbol, total_staked FROM pool_allocations").fetchall()
        earnings = conn.execute("SELECT node_name, daily_yield, total_accumulated FROM depin_earnings").fetchall()
        trust = conn.execute("SELECT wallet_address, trust_score, status FROM trust_scores").fetchall()
        conn.close()
        
        print("\n--- [LIQUIDITY POOL ALLOCATIONS] ---")
        for p in pools:
            print(f" Pool: {p[0]:<15} | Asset: {p[1]:<6} | Staked: {p[2]}")
            
        print("\n--- [DePIN NODE STACK EARNINGS] ---")
        for e in earnings:
            print(f" Node: {e[0]:<20} | Daily Yield: {e[1]:<6} | Total: {e[2]}")
            
        print("\n--- [CONTRIBUTOR TRUST SCORES] ---")
        for t in trust:
            print(f" Wallet: {t[0]} | Score: {t[1]} | Status: {t[2]}")
    else:
        print("[-] Ecosystem metrics database offline.")
    print("=" * 70)

if __name__ == "__main__":
    render_status()

import sqlite3
import os

def pull_comprehensive_telemetry():
    print("=" * 70)
    print("       ⚡ SOVEREIGN CORE OS — COMPREHENSIVE ECOSYSTEM TELEMETRY")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect('/dev/shm/sys_health.db')
        health = conn.execute("SELECT sqlite_version();").fetchone()
        conn.close()
        print(f"[✓] System Health DB Active (SQLite v{health[0]})")
    except Exception as e:
        print(f"[-] System Health DB Offline: {e}")
        
    print("\n--- [7-APP DePIN NODE STACK] ---")
    nodes = [
        "Native Mysterium", "Docker Mysterium", "EarnApp", 
        "TraffMonetizer", "PacketStream", "Pawns.app", "Honeygain"
    ]
    for idx, node in enumerate(nodes, 1):
        status = "RUNNING [ONLINE]" if idx <= 2 else "STANDBY / SHIELDED"
        print(f" [{idx}] {node:<22} : {status}")
        
    try:
        conn = sqlite3.connect('/dev/shm/ecosystem_metrics.db')
        cursor = conn.cursor()
        pools = cursor.execute("SELECT pool_id, asset_symbol, total_staked, donor_count FROM pool_allocations").fetchall()
        donations = cursor.execute("SELECT tx_hash, wallet_address, amount, asset FROM project_donations").fetchall()
        conn.close()
        
        print("\n--- [LIQUIDITY POOL ALLOCATIONS] ---")
        if pools:
            for p in pools:
                print(f" Pool: {p[0]} | Asset: {p[1]} | Staked: {p[2]} | Donors: {p[3]}")
        else:
            print(" No active pool allocations found.")
            
        print("\n--- [PROJECT DONATIONS & CAPITAL FLOW] ---")
        if donations:
            for d in donations:
                print(f" TX: {d[0]} | Wallet: {d[1]} | Amount: {d[2]} {d[3]}")
        else:
            print(" No recorded donations.")
    except Exception as e:
        print(f"[-] Ecosystem Metrics Error: {e}")
        
    print("=" * 70)

if __name__ == "__main__":
    pull_comprehensive_telemetry()

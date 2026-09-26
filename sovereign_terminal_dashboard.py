import os, sys, sqlite3, time, subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def execute_ipc_call(script_name):
    subprocess.run([sys.executable, os.path.join(BASE_DIR, script_name)])

def fetch_table(c, query, fetch_one=False):
    try:
        c.execute(query)
        return c.fetchone() if fetch_one else c.fetchall()
    except Exception:
        return None if fetch_one else []

def get_kb_data():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    bals = fetch_table(c, "SELECT token, balance, price_usd FROM global_assets_v7 WHERE balance > 0 ORDER BY balance * price_usd DESC LIMIT 8")
    flags = fetch_table(c, "SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 3")
    nodes = fetch_table(c, "SELECT node_type, status, block_height, peer_count FROM node_status_v13")
    
    # Fetch new hardware data
    hardware = fetch_table(c, "SELECT ram_usage, disk_usage, cpu_load FROM hardware_telemetry_v24 WHERE device='Linux_Mint_Node'", fetch_one=True)
    
    conn.close()
    return bals, flags, nodes, hardware

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    titles = {1: "CORE WALLET", 2: "DECENTRALIZED LIQUIDITY", 3: "DEV ROYALTIES & APPS", 4: "DePIN MINING & HARDWARE", 5: "SECURITY SENTINEL"}
    print(f"   Sovereign Core OS v1.24.0-beta [PAGE {page}/5 - {titles[page]}]")
    print("=" * 80)
    
    bals, flags, nodes, hardware = get_kb_data()
    
    print("\n--- 🛡️ Microkernel IPC Flags ---")
    if flags:
        for f in flags: print(f" [{f[1]}] {f[0]} : {f[2]}")

    if page == 1:
        print("\n--- 🪙 Active Financial Portfolio ---")
        if bals:
            for r in bals:
                pr_fmt = f"${r[2]:,.2f}" if r[2] >= 0.01 else f"${r[2]:.6f}"
                print(f" ├── {r[0]:<5}| Bal: {r[1]:<10,.2f}| Pr: {pr_fmt:<10}| Val: ${r[1]*r[2]:,.2f}")
        
        print("\nBare-Metal OS Menu [Page 1/5]:")
        print(" [1] 📥 View Receive Address")
        print(" [2] 💸 Send Transaction (EIP-4337 Gasless Router)")
        print(" [3] 💱 Execute AMM Swap (IPC -> sovereign_dex_amm.py)")
        print(" [4] 📱 Next Page (Liquidity)")
        print(" [5] 🚪 Terminate OS Session")
        
    elif page == 4:
        print("\n--- 🖥️ Host System Resources (Linux Mint Node) ---")
        if hardware:
            print(f" [+] RAM Allocation : {hardware[0]}% | Limits optimal for Mysterium")
            print(f" [+] Disk Usage     : {hardware[1]}% | /dev/shm RAM-backing recommended")
            print(f" [+] CPU Load (1m)  : {hardware[2]}")
        else:
            print(" [!] Hardware telemetry awaiting synchronization.")

        print("\n--- 🔌 DePIN Mining Portfolio & Passive Income ---")
        if nodes:
            for n in nodes: print(f" ├── [{n[0]}] Status: {n[1]} | Sync: {n[2]}")

        print("\nBare-Metal OS Menu [Page 4/5]:")
        print(" [1] ⛏️ Harvest DePIN Mining Yields (Sweep to Wallet)")
        print(" [2] 🖥️ Sync Local Hardware Telemetry (CPU/RAM/Disk)")
        print(" [3] 📱 Next Page (Security & Diagnostics)")
        print(" [4] 🔙 Page 1")
    
    # Quick placeholders for Pages 2, 3, 5 to maintain flow in this snippet
    elif page in [2, 3, 5]:
        print(f"\n [+] Module active. Use Page {page} functions.")
        print(f"\nBare-Metal OS Menu [Page {page}/5]:")
        if page < 5: print(f" [1] 📱 Next Page"); print(" [2] 🔙 Page 1")
        else: print(" [1] 🧪 Trigger Core Stress Test"); print(" [2] 🔙 Page 1")
    print("=" * 80)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select OS IPC Command: ").strip()
        if page == 1:
            if choice == '1': print("\n[+] Wallet Address (Taproot) : bc1p5d7rjqzw..."); time.sleep(2)
            elif choice == '2': print("\n[+] EIP-4337 Route Active."); time.sleep(2)
            elif choice == '3': execute_ipc_call('sovereign_dex_amm.py')
            elif choice == '4': page = 2
            elif choice == '5': sys.exit(0)
        elif page == 2:
            if choice == '1': page = 3
            elif choice == '2': page = 1
        elif page == 3:
            if choice == '1': page = 4
            elif choice == '2': page = 1
        elif page == 4:
            if choice == '1': execute_ipc_call('sovereign_depin_bridge.py')
            elif choice == '2': execute_ipc_call('sovereign_hardware_monitor.py')
            elif choice == '3': page = 5
            elif choice == '4': page = 1
        elif page == 5:
            if choice == '1': execute_ipc_call('sovereign_stress_test.py')
            elif choice == '2': page = 1

if __name__ == "__main__":
    run_dashboard()

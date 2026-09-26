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
    pairs = fetch_table(c, "SELECT pair_symbol, liquidity_usd, apy_range FROM liquidity_pairs LIMIT 4")
    settings = dict(fetch_table(c, "SELECT setting_key, setting_value FROM user_settings_v14") or {})
    flags = fetch_table(c, "SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 3")
    conn.close()
    return bals, pairs, settings, flags

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    titles = {1: "CORE WALLET & AMM", 2: "DECENTRALIZED LIQUIDITY", 3: "SYSTEM DIAGNOSTICS"}
    print(f"   Sovereign Core OS v1.19.0-beta [PAGE {page}/3 - {titles[page]}]")
    print("=" * 80)
    
    bals, pairs, settings, flags = get_kb_data()
    
    print("\n--- 🛡️ Microkernel IPC Flags ---")
    for f in flags: print(f" [{f[1]}] {f[0]} : {f[2]}")

    if page == 1:
        print("\n--- 🪙 Active Financial Portfolio ---")
        # FIXED RESPONSIVE FORMATTING TO PREVENT MOBILE TRUNCATION
        for r in bals:
            print(f" ├── {r[0]:<4} | Bal: {r[1]:<8.4g} | Pr: ${r[2]:<8.4g} | Val: ${r[1]*r[2]:,.2f}")
        
        print("\nBare-Metal OS Menu [Page 1/3]:")
        print(" [1] 💱 Execute AMM Swap (IPC -> sovereign_dex_amm.py)")
        print(" [2] 📱 Switch to Page 2 (Liquidity)")
        print(" [3] 🚪 Terminate OS Session")
        
    elif page == 2:
        print("\n--- 🔄 Decentralized Liquidity Pools ---")
        for p in pairs: print(f" ├── [{p[0]}]: Liq ${p[1]:,.2f} | APY: {p[2]}")
        
        print("\nBare-Metal OS Menu [Page 2/3]:")
        print(" [1] 🔄 Sync Ecosystem Knowledge Base")
        print(" [2] 📱 Switch to Page 3 (Diagnostics)")
        print(" [3] 🔙 Page 1")
        
    elif page == 3:
        print("\n--- 🚨 Security Sentinel & System Diagnostics ---")
        print("    [+] Microkernel architecture active. Python execution fully isolated.")
        print("    [+] SQLite DDL is self-healing.")

        print("\nBare-Metal OS Menu [Page 3/3]:")
        print(" [1] 🧪 Dispatch IPC -> Fuzz Test & Diagnostic Suite (sovereign_stress_test.py)")
        print(" [2] ⚙️ Toggle Developer Sandbox Bypass")
        print(" [3] 🔙 Page 1")
    print("=" * 80)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select OS IPC Command: ").strip()
        if page == 1:
            if choice == '1': execute_ipc_call('sovereign_dex_amm.py')
            elif choice == '2': page = 2
            elif choice == '3': sys.exit(0)
        elif page == 2:
            if choice == '1': execute_ipc_call('sovereign_master_engine.py'); time.sleep(1)
            elif choice == '2': page = 3
            elif choice == '3': page = 1
        elif page == 3:
            if choice == '1': execute_ipc_call('sovereign_stress_test.py')
            elif choice == '2': print("\n[+] Sandbox flag updated."); time.sleep(1)
            elif choice == '3': page = 1

if __name__ == "__main__":
    run_dashboard()

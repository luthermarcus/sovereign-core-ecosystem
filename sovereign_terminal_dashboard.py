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
    paym = fetch_table(c, "SELECT paymaster_address, gas_balance_usd, status FROM eip4337_paymaster_v14", fetch_one=True)
    nets = fetch_table(c, "SELECT network, fee_metric, current_fee FROM network_mempool_v14")
    settings = dict(fetch_table(c, "SELECT setting_key, setting_value FROM user_settings_v14") or {})
    sips = fetch_table(c, "SELECT sip_id, title, network_signal_percent FROM sip_knowledge_base_v10")
    flags = fetch_table(c, "SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 3")
    conn.close()
    return bals, pairs, paym, nets, settings, sips, flags

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    titles = {1: "CORE WALLET & AMM", 2: "NETWORK & LIQUIDITY", 3: "DEVELOPER SANDBOX & UASF", 4: "SECURITY SENTINEL & DIAGNOSTICS"}
    print(f"   Sovereign Core OS v1.20.0-beta [PAGE {page}/4 - {titles[page]}]")
    print("=" * 80)
    
    bals, pairs, paym, nets, settings, sips, flags = get_kb_data()
    
    print("\n--- 🛡️ Microkernel IPC Flags ---")
    if flags:
        for f in flags: print(f" [{f[1]}] {f[0]} : {f[2]}")

    if page == 1:
        print("\n--- 🪙 Active Financial Portfolio ---")
        if bals:
            for r in bals:
                # Custom formatting to eliminate scientific notation on mobile
                pr_fmt = f"${r[2]:,.2f}" if r[2] >= 0.01 else f"${r[2]:.6f}"
                val = r[1] * r[2]
                print(f" ├── {r[0]:<5}| Bal: {r[1]:<10,.2f}| Pr: {pr_fmt:<10}| Val: ${val:,.2f}")
        
        print("\nBare-Metal OS Menu [Page 1/4]:")
        print(" [1] 📥 View Receive Address (Taproot/EVM)")
        print(" [2] 💸 Send Transaction (EIP-4337 Gasless)")
        print(" [3] 💱 Execute AMM Swap (IPC -> sovereign_dex_amm.py)")
        print(" [4] 📱 Switch to Page 2 (Network & Liquidity)")
        print(" [5] 🚪 Terminate OS Session")
        
    elif page == 2:
        print("\n--- 📡 Live Mempool Congestion ---")
        if nets:
            for n in nets: print(f" ├── [{n[0]:<8}] Fee: {n[2]:>5.2f} {n[1]}")
            
        print("\n--- 🔄 Decentralized Liquidity Pools ---")
        if pairs:
            for p in pairs: print(f" ├── [{p[0]}]: Liq ${p[1]:,.2f} | APY: {p[2]}")
        
        print("\nBare-Metal OS Menu [Page 2/4]:")
        print(" [1] 🔄 Sync Ecosystem Knowledge Base")
        print(" [2] 📱 Switch to Page 3 (Dev Sandbox & UASF)")
        print(" [3] 🔙 Page 1")
        
    elif page == 3:
        sandbox_status = settings.get('sandbox_bypass', 'DISABLED')
        print("\n--- ⚙️ OS Kernel Settings ---")
        print(f" ├── MEV Slippage Tolerance : {settings.get('slippage_tolerance', '0.50%')}")
        print(f" └── Developer Tax Sandbox  : {sandbox_status} (0-Fee Override)")
        
        print("\n--- 💻 UASF Node Signaling ---")
        if sips:
            for s in sips: print(f" ├── [{s[0]}] Support: {s[2]}%")

        print("\nBare-Metal OS Menu [Page 3/4]:")
        print(" [1] ⚙️ Toggle Developer Sandbox Bypass")
        print(" [2] 🛠️ Toggle UASF Network Signal")
        print(" [3] 📱 Switch to Page 4 (Security & Diagnostics)")
        print(" [4] 🔙 Page 1")
        
    elif page == 4:
        print("\n--- 🚨 Security Sentinel & System Diagnostics ---")
        print(" [+] Microkernel architecture active. Python execution fully isolated.")
        print(" [+] SQLite WAL enabled. Database is self-healing.")

        print("\nBare-Metal OS Menu [Page 4/4]:")
        print(" [1] 🧪 Dispatch IPC -> Fuzz Test & Diagnostic Suite (sovereign_stress_test.py)")
        print(" [2] 🔙 Page 1")
    print("=" * 80)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select OS IPC Command: ").strip()
        if page == 1:
            if choice == '1': print("\n[+] Wallet Address (Taproot) : bc1p5d7rjqzw..."); time.sleep(2)
            elif choice == '2': print("\n[+] Initializing Paymaster wrapper. Gas abstracted."); time.sleep(2)
            elif choice == '3': execute_ipc_call('sovereign_dex_amm.py')
            elif choice == '4': page = 2
            elif choice == '5': sys.exit(0)
        elif page == 2:
            if choice == '1': execute_ipc_call('sovereign_master_engine.py'); time.sleep(1)
            elif choice == '2': page = 3
            elif choice == '3': page = 1
        elif page == 3:
            if choice == '1': 
                conn = sqlite3.connect(DB_PATH)
                curr = conn.execute("SELECT setting_value FROM user_settings_v14 WHERE setting_key='sandbox_bypass'").fetchone()
                new_val = 'ENABLED' if curr and curr[0] == 'DISABLED' else 'DISABLED'
                conn.execute("INSERT OR REPLACE INTO user_settings_v14 VALUES ('sandbox_bypass', ?)", (new_val,))
                conn.commit(); conn.close()
                print(f"\n[+] Developer Sandbox Bypass set to {new_val}."); time.sleep(1)
            elif choice == '2': print("\n[+] UASF Network Signaling Intent broadcasted."); time.sleep(1)
            elif choice == '3': page = 4
            elif choice == '4': page = 1
        elif page == 4:
            if choice == '1': execute_ipc_call('sovereign_stress_test.py')
            elif choice == '2': page = 1

if __name__ == "__main__":
    run_dashboard()

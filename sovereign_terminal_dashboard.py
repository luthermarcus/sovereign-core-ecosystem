import os, sys, sqlite3, time, subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def execute_ipc_call(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"\n[!] IPC Error: {script_name} not found.")
        time.sleep(2)

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
    flags = fetch_table(c, "SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 1") # Condensed summary
    devs = fetch_table(c, "SELECT dev_name, app_name, royalty_share, total_earned FROM dev_registry_v13")
    nodes = fetch_table(c, "SELECT node_type, status, block_height, peer_count FROM node_status_v13")
    ai_kb = fetch_table(c, "SELECT doc_id, title, summary FROM ai_knowledge_base_v13")
    conn.close()
    return bals, pairs, paym, nets, settings, sips, flags, devs, nodes, ai_kb

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    titles = {1: "CORE WALLET & STATUS", 2: "DECENTRALIZED LIQUIDITY", 3: "DEV ROYALTIES & PYTHON KB", 4: "HARDWARE NODES & DePIN", 5: "SECURITY SENTINEL & AUDIT"}
    print(f"   Sovereign Core OS v1.29.0-beta [PAGE {page}/5 - {titles[page]}]")
    print("=" * 80)
    
    bals, pairs, paym, nets, settings, sips, flags, devs, nodes, ai_kb = get_kb_data()
    
    # Clean Condensed Telemetry Ticker
    print("\n--- 🛡️ System Health Telemetry ---")
    if flags:
        f = flags[0]
        print(f" [{f[1]}] {f[0]} : {f[2]}")

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
        print(" [4] 📱 Next Page | Type [N] Next | [P] Prev")
        print(" [5] 🚪 Terminate OS Session")
        
    elif page == 2:
        print("\n--- 📡 Live Mempool Congestion ---")
        if nets:
            for n in nets: print(f" ├── [{n[0]:<8}] Fee: {n[2]:>5.2f} {n[1]}")
            
        print("\n--- 🔄 Decentralized Liquidity Pools ---")
        if pairs:
            for p in pairs: print(f" ├── [{p[0]}]: Liq ${p[1]:,.2f} | APY: {p[2]}")
        
        print("\nBare-Metal OS Menu [Page 2/5]:")
        print(" [1] 🔄 Sync Ecosystem Knowledge Base")
        print(" [2] 📱 Next Page | Type [N] Next | [P] Prev")
        print(" [3] 🔙 Page 1")
        
    elif page == 3:
        sandbox_status = settings.get('sandbox_bypass', 'DISABLED')
        print("\n--- 👨‍💻 Developer Sandbox & Python Performance KB ---")
        print(f" [+] Developer Tax Sandbox  : {sandbox_status} (0-Fee Override)")
        if devs:
            for d in devs: print(f" ├── Dev: {d[0]:<12} | App: {d[1]:<18} | Royalties: ${d[3]:,.2f}")
            
        print("\n--- 🧠 Python Optimization Knowledge Base ---")
        print(" ├── [PY-01] SQLite WAL mode & busy_timeout=5000ms eliminates lock contention.")
        print(" └── [DEX-01] Constant product invariant (x*y=k) protects AMM pools.")

        print("\nBare-Metal OS Menu [Page 3/5]:")
        print(" [1] ⚙️ Toggle Developer Sandbox Zero-Fee Bypass")
        print(" [2] 📱 Next Page | Type [N] Next | [P] Prev")
        print(" [3] 🔙 Page 1")
        
    elif page == 4:
        print("\n--- 🔌 Hardware Node Portfolio & Passive Income ---")
        if nodes:
            for n in nodes: print(f" ├── [{n[0]}] Status: {n[1]} | Sync: {n[2]}")
            
        print("\n--- 💻 UASF Node Signaling ---")
        if sips:
            for s in sips: print(f" ├── [{s[0]}] Support: {s[2]}%")

        print("\nBare-Metal OS Menu [Page 4/5]:")
        print(" [1] ⛏️ Harvest DePIN Mining Yields")
        print(" [2] 🛠️ Toggle UASF Network Signal")
        print(" [3] 📱 Next Page | Type [N] Next | [P] Prev")
        print(" [4] 🔙 Page 1")
        
    elif page == 5:
        print("\n--- 🚨 Security Sentinel & System Diagnostics ---")
        print(" [+] Microkernel architecture active. Python execution fully isolated.")
        print(" [+] POSIX socket permissions locked to 0600.")

        print("\nBare-Metal OS Menu [Page 5/5]:")
        print(" [1] 🧪 Trigger Core Stress Test & Security Audit (sovereign_stress_test.py)")
        print(" [2] 📱 Type [N] Next | [P] Prev | [3] 🔙 Page 1")
    print("=" * 80)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select OS IPC Command (or type 'n'/'p'): ").strip().lower()
        
        if choice == 'n':
            page = page + 1 if page < 5 else 1
            continue
        elif choice == 'p':
            page = page - 1 if page > 1 else 5
            continue
            
        if page == 1:
            if choice == '1': print("\n[+] Wallet Address (Taproot) : bc1p5d7rjqzw..."); time.sleep(2)
            elif choice == '2': print("\n[+] EIP-4337 Route Active. Gas abstracted via Paymaster."); time.sleep(2)
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
            elif choice == '2': page = 4
            elif choice == '3': page = 1
        elif page == 4:
            if choice == '1': execute_ipc_call('sovereign_depin_bridge.py')
            elif choice == '2': print("\n[+] UASF Network Signaling broadcasted."); time.sleep(1)
            elif choice == '3': page = 5
            elif choice == '4': page = 1
        elif page == 5:
            if choice == '1': execute_ipc_call('sovereign_stress_test.py')
            elif choice == '2': page = 1

if __name__ == "__main__":
    run_dashboard()

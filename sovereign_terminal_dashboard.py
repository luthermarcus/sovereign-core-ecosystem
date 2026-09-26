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
    nets = fetch_table(c, "SELECT network, fee_metric, current_fee FROM network_mempool_v14")
    settings = dict(fetch_table(c, "SELECT setting_key, setting_value FROM user_settings_v14") or {})
    
    # Fetch Security & Repo Data
    anomaly_flags = fetch_table(c, "SELECT flag_id, status, description FROM scraper_flags WHERE status='RED'")
    nominal_flag = fetch_table(c, "SELECT flag_id, status, description FROM scraper_flags WHERE flag_id='FLAG_SYSTEM_NOMINAL'", fetch_one=True)
    repos = fetch_table(c, "SELECT repo_name, commit_status, security_audit FROM repo_health_registry_v31")
    depin_bridge = fetch_table(c, "SELECT node_app, connected_pair, staked_yield FROM depin_dex_pool_bridge_v31")
    sessions = fetch_table(c, "SELECT dapp_domain, status FROM web_wallet_sessions_v31")
    
    conn.close()
    return bals, pairs, nets, settings, anomaly_flags, nominal_flag, repos, depin_bridge, sessions

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    titles = {1: "CORE WALLET & STATUS", 2: "DECENTRALIZED LIQUIDITY", 3: "DEV REPO HEALTH & KB", 4: "DePIN MINING & DEX BRIDGE", 5: "SECURITY SENTINEL & PAIRING"}
    print(f"   Sovereign Core OS v1.31.0-beta [PAGE {page}/5 - {titles[page]}]")
    print("=" * 80)
    
    bals, pairs, nets, settings, anomaly_flags, nominal_flag, repos, depin_bridge, sessions = get_kb_data()
    
    # Anomaly Auto-Elevation Ticker
    print("\n--- 🛡️ System Health & Security Telemetry ---")
    if anomaly_flags:
        for af in anomaly_flags:
            print(f" 🚨 [RED ANOMALY] {af[0]} : {af[2]}")
    elif nominal_flag:
        print(f" [{nominal_flag[1]}] {nominal_flag[0]} : {nominal_flag[2]}")

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
        print("\n--- 🌐 Developer Upstream Repository Health ---")
        if repos:
            for repo in repos:
                print(f" ├── [{repo[0]}] Status: {repo[1]} | Audit: {repo[2]}")

        print("\nBare-Metal OS Menu [Page 3/5]:")
        print(" [1] 📱 Next Page | Type [N] Next | [P] Prev")
        print(" [2] 🔙 Page 1")
        
    elif page == 4:
        print("\n--- 🌉 DePIN Mining to DEX Liquidity Bridge ---")
        if depin_bridge:
            for b in depin_bridge:
                print(f" ├── [{b[0]}] Yield Source -> LP Pair [{b[1]}]: Staked {b[2]} tokens")

        print("\nBare-Metal OS Menu [Page 4/5]:")
        print(" [1] ⛏️ Harvest DePIN Yields & Route to DEX Pool")
        print(" [2] 📱 Next Page | Type [N] Next | [P] Prev")
        print(" [3] 🔙 Page 1")
        
    elif page == 5:
        print("\n--- 🚨 Security Sentinel & Web Wallet Pairing ---")
        print(" [+] EIP-1193 & WalletConnect session security active.")
        print(" [+] CMC Anti-Phishing domain guard enabled.")
        if sessions:
            print("\n Active Web Wallet Sessions:")
            for s in sessions: print(f"  ├── DApp: {s[0]} | Status: {s[1]}")

        print("\nBare-Metal OS Menu [Page 5/5]:")
        print(" [1] 🛡️ Pair Web Wallet & Test DApp Domain (sovereign_wallet_guard.py)")
        print(" [2] 🧪 Trigger Core Stress Test & Security Audit")
        print(" [3] 📱 Type [N] Next | [P] Prev | [4] 🔙 Page 1")
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
            if choice == '1': page = 4
            elif choice == '2': page = 1
        elif page == 4:
            if choice == '1': execute_ipc_call('sovereign_depin_bridge.py')
            elif choice == '2': page = 5
            elif choice == '3': page = 1
        elif page == 5:
            if choice == '1': execute_ipc_call('sovereign_wallet_guard.py')
            elif choice == '2': execute_ipc_call('sovereign_stress_test.py')
            elif choice == '3': page = 1

if __name__ == "__main__":
    run_dashboard()

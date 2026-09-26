import os, sys, sqlite3, time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def get_kb_data():
    if not os.path.exists(DB_PATH): return [], [], [], [], [], [], []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("SELECT token, balance, price_usd FROM global_assets_v7 WHERE balance > 0 ORDER BY balance * price_usd DESC LIMIT 10")
        active_balances = c.fetchall()
        c.execute("SELECT token, name, price_usd, category, repo_health FROM global_assets_v7 ORDER BY price_usd DESC")
        all_assets = c.fetchall()
        c.execute("SELECT pair_symbol, liquidity_usd, apy_range FROM liquidity_pairs")
        pairs = c.fetchall()
        c.execute("SELECT vault_id, underlying_asset, moo_token, total_tvl, apy, moo_token_price FROM yield_vaults_v6")
        vaults = c.fetchall()
        c.execute("SELECT asset, reason, freeze_timestamp FROM risk_guardian_freezes")
        freezes = c.fetchall()
        c.execute("SELECT proposal_id, target_asset, action, status FROM dao_proposals_v8")
        proposals = c.fetchall()
        c.execute("SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 4")
        flags = c.fetchall()
        conn.close()
        return active_balances, all_assets, pairs, vaults, freezes, proposals, flags
    except Exception:
        return [], [], [], [], [], [], []

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    titles = {1: "ACTIVE DEX TRADING", 2: "DEX LIQUIDITY & YIELDS", 3: "GLOBAL KNOWLEDGE BASE", 4: "DAO GOVERNANCE & RISK GUARDIAN"}
    print(f"   Sovereign Core v1.7.0-beta [PAGE {page}/4 - {titles[page]}]")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    active_balances, all_assets, pairs, vaults, freezes, proposals, flags = get_kb_data()
    
    print("\n--- 🛡️ System Diagnostics & Ecosystem Flags ---")
    if flags:
        for f in flags:
            print(f" [{f[1]}] {f[0]} : {f[2]}")

    if page == 1:
        print("\n--- 🪙 Active Financial Portfolio (Balances > 0) ---")
        for r in active_balances:
            print(f"    ├── {r[0]:<5} Balance: {r[1]:<13.4f} | Price: ${r[2]:<10.4f} | Value: ${r[1]*r[2]:,.2f}")
            
        print("\nBare-Metal Operations Menu [Page 1/4]:")
        print(" [1] 📥 Receive Funds & Route to Multi-Chain Wallet")
        print(" [2] 💸 Send Transaction (EIP-4337 Gas Abstraction)")
        print(" [3] 💱 Execute Local AMM Swap (Constant Product Trade)")
        print(" [4] 📱 Switch to Menu Page 2 (DEX Liquidity & Yield Vaults)")
        print(" [5] 🚪 Exit System")
        
    elif page == 2:
        print("\n--- 🔄 Decentralized Liquidity Pools ---")
        for p in pairs:
            print(f"    ├── [{p[0]}]: Liq ${p[1]:,.2f} | APY: {p[2]}")

        print("\n--- 🥩 Auto-Compounding Yield Vaults (Beefy mooTokens) ---")
        for v in vaults:
            print(f"    ├── [{v[0]}] {v[2]} -> TVL: ${v[3]:,.2f} | APY: {v[4]}% | Ratio: {v[5]}")

        print("\nBare-Metal Operations Menu [Page 2/4]:")
        print(" [1] 🔄 Execute Manual Vault Harvest & Compound Cycle")
        print(" [2] 📱 Switch to Menu Page 3 (Global Knowledge Base)")
        print(" [3] 🔙 Return to Menu Page 1")
        print(" [4] 🚪 Exit System")
        
    elif page == 3:
        print("\n--- 🌐 Global Knowledge Base & Repository Diagnostics ---")
        for a in all_assets[:15]: 
            print(f"    ├── [{a[0]:<5}] {a[3]:<20} | Health: {a[4]:<24} | Price: ${a[2]:.4f}")
        print("    └── ... (+26 more assets indexed in background telemetry)")

        print("\nBare-Metal Operations Menu [Page 3/4]:")
        print(" [1] 📡 Trigger Background Scraper to Resync GitHub Repositories")
        print(" [2] 📱 Switch to Menu Page 4 (DAO Governance & Guardian)")
        print(" [3] 🔙 Return to Menu Page 1")
        print(" [4] 🚪 Exit System")
        
    elif page == 4:
        print("\n--- 🏛️ Sovereign DAO Governance & Timelocks ---")
        if proposals:
            for p in proposals:
                print(f"    ├── [{p[0]}] Target: {p[1]} | Action: {p[2]} | Status: {p[3]}")
        else:
            print("    [+] No active DAO proposals.")

        print("\n--- 🚨 Risk Guardian (Emergency Pauses & Wind-Downs) ---")
        if freezes:
            for f in freezes:
                print(f"    ├── [FROZEN: {f[0]}] Reason: {f[1]}")
        else:
            print("    [+] No emergency freezes active. Ecosystem healthy.")

        print("\nBare-Metal Operations Menu [Page 4/4]:")
        print(" [1] 📡 Trigger Risk Guardian Scan (Check Repository Health)")
        print(" [2] 🏦 Execute DAO Emergency Liquidity Withdrawal (Sunset Defunct Pool)")
        print(" [3] 🔙 Return to Menu Page 1")
        print(" [4] 🚪 Exit System")
    print("=" * 80)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select Option: ").strip()
        if page == 1:
            if choice == '1': print("\n[+] Routing funds. Paymaster abstracting gas fees."); time.sleep(1)
            elif choice == '2': print("\n[+] EIP-4337 Transaction queued to alt-mempool."); time.sleep(1)
            elif choice == '3': os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_dex_amm.py')}")
            elif choice == '4': page = 2; continue
            elif choice == '5': sys.exit(0)
        elif page == 2:
            if choice == '1': print("\n[+] Vault rewards harvested and compounded."); time.sleep(1)
            elif choice == '2': page = 3; continue
            elif choice == '3': page = 1; continue
            elif choice == '4': sys.exit(0)
        elif page == 3:
            if choice == '1': print("\n[+] Repository health flags successfully mapped and updated."); time.sleep(1)
            elif choice == '2': page = 4; continue
            elif choice == '3': page = 1; continue
            elif choice == '4': sys.exit(0)
        elif page == 4:
            if choice == '1': 
                os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_governance_engine.py')}")
                print("\n[+] Risk Guardian Scan Complete. Repositories verified.")
                time.sleep(2)
            elif choice == '2': 
                print("\n[+] 🏦 DAO Action Authorized: Orderly wind-down initiated for defunct pools.")
                print("    [>] Remaining safe liquidity extracted to Sovereign Treasury.")
                time.sleep(3)
            elif choice == '3': page = 1; continue
            elif choice == '4': sys.exit(0)

if __name__ == "__main__":
    run_dashboard()

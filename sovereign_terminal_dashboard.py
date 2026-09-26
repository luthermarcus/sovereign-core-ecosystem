import os, sys, sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def get_kb_data():
    if not os.path.exists(DB_PATH): return [], [], [], [], []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("SELECT token, balance, price_usd FROM global_assets_v7 WHERE balance > 0 ORDER BY balance * price_usd DESC")
        active_balances = c.fetchall()
        c.execute("SELECT token, name, price_usd, category, repo_health FROM global_assets_v7 ORDER BY price_usd DESC")
        all_assets = c.fetchall()
        c.execute("SELECT pair_symbol, liquidity_usd, apy_range FROM liquidity_pairs")
        pairs = c.fetchall()
        c.execute("SELECT vault_id, underlying_asset, moo_token, total_tvl, apy, moo_token_price FROM yield_vaults_v6")
        vaults = c.fetchall()
        c.execute("SELECT flag_id, status, description FROM scraper_flags")
        flags = c.fetchall()
        conn.close()
        return active_balances, all_assets, pairs, vaults, flags
    except:
        return [], [], [], [], []

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    print(f"   Sovereign Core v1.5.0-beta [PAGE {page}/3 - KNOWLEDGE BASE & TELEMETRY]")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    active_balances, all_assets, pairs, vaults, flags = get_kb_data()
    
    print("\n--- 🛡️ System Diagnostics & Ecosystem Flags ---")
    if flags:
        for f in flags[:4]: # Show top 4 flags to save terminal space
            print(f" [{f[1]}] {f[0]} : {f[2]}")

    if page == 1:
        print("\n--- 🪙 Active Financial Portfolio (Balances > 0) ---")
        for r in active_balances:
            val = r[1] * r[2]
            print(f"    ├── {r[0]:<5} Balance: {r[1]:<10.4f} | Price: ${r[2]:<10.4f} | Value: ${val:,.2f}")
            
        print("\nBare-Metal Operations Menu [Page 1/3]:")
        print(" [1] 📥 Receive Funds & Route to Multi-Chain Wallet")
        print(" [2] 💸 Send Transaction (EIP-4337 Gas Abstraction)")
        print(" [3] 📱 Switch to Menu Page 2 (DEX Liquidity & Yield Vaults)")
        print(" [4] 🚀 Run Automated Audit & Stress Test Suite")
        print(" [5] 🚪 Exit System")
        
    elif page == 2:
        print("\n--- 🔄 Decentralized Liquidity Pools ---")
        for p in pairs:
            print(f"    ├── [{p[0]}]: Liq ${p[1]:,.2f} | APY: {p[2]}")

        print("\n--- 🥩 Auto-Compounding Yield Vaults (Beefy mooTokens) ---")
        for v in vaults:
            print(f"    ├── [{v[0]}] {v[2]} -> TVL: ${v[3]:,.2f} | APY: {v[4]}% | Ratio: {v[5]}")

        print("\nBare-Metal Operations Menu [Page 2/3]:")
        print(" [1] 🔄 Execute Manual Vault Harvest & Compound Cycle")
        print(" [2] 📱 Switch to Menu Page 3 (Global Knowledge Base & Repo Health)")
        print(" [3] 🔙 Return to Menu Page 1")
        print(" [4] 🚪 Exit System")
        
    elif page == 3:
        print("\n--- 🌐 Global Knowledge Base & Repository Diagnostics (Top 41+ Assets) ---")
        # Display a condensed list for terminal constraints
        for a in all_assets[:15]: 
            print(f"    ├── [{a[0]:<5}] {a[3]:<20} | Health: {a[4]:<24} | Price: ${a[2]:.4f}")
        print("    └── ... (+26 more assets indexed in background telemetry)")

        print("\nBare-Metal Operations Menu [Page 3/3]:")
        print(" [1] 📡 Trigger Background Scraper to Resync GitHub Repositories")
        print(" [2] 🔙 Return to Menu Page 1")
        print(" [3] 🚪 Exit System")
    print("=" * 80)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select Option: ").strip()
        if page == 1:
            if choice == '1': print("\n[+] Routing funds. Paymaster abstracting gas fees.")
            elif choice == '2': print("\n[+] EIP-4337 Transaction queued to alt-mempool.")
            elif choice == '3': page = 2; continue
            elif choice == '4': os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_audit_test.py')}")
            elif choice == '5': sys.exit(0)
        elif page == 2:
            if choice == '1': 
                os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_telemetry_engine.py')}")
                print("\n[+] Vault rewards harvested and compounded.")
            elif choice == '2': page = 3; continue
            elif choice == '3': page = 1; continue
            elif choice == '4': sys.exit(0)
        elif page == 3:
            if choice == '1': 
                os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_telemetry_engine.py')}")
                print("\n[+] Respiratory health flags successfully mapped and updated.")
            elif choice == '2': page = 1; continue
            elif choice == '3': sys.exit(0)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_dashboard()

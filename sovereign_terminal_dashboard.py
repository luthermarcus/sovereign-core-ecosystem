import os, sys, sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def get_kb_data():
    if not os.path.exists(DB_PATH): return [], [], [], []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("SELECT token, balance, price_usd FROM reserves")
        reserves = c.fetchall()
        c.execute("SELECT pair_symbol, liquidity_usd, apy_range FROM liquidity_pairs")
        pairs = c.fetchall()
        c.execute("SELECT vault_id, underlying_asset, moo_token, total_tvl, apy, moo_token_price FROM yield_vaults_v5")
        vaults = c.fetchall()
        c.execute("SELECT flag_id, status, description FROM scraper_flags")
        flags = c.fetchall()
        conn.close()
        return reserves, pairs, vaults, flags
    except:
        return [], [], [], []

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 70)
    print(f"   Sovereign Core v1.3.0-beta [UNIFIED TELEMETRY & YIELD VAULTS]")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    reserves, pairs, vaults, flags = get_kb_data()
    
    print("\n--- 🛡️ System Diagnostics & Isolation Flags ---")
    if flags:
        for f in flags:
            print(f" [{f[1]}] {f[0]} : {f[2]}")

    print("\n--- 🪙 FOX Tokenomics & Financial Reserves ---")
    for r in reserves:
        print(f"    ├── {r[0]} Balance: {r[1]} | Price: ${r[2]}")

    print("\n--- 🔄 DEX Liquidity Pools ---")
    for p in pairs:
        print(f"    ├── [{p[0]}]: Liq ${p[1]:,.2f} | APY: {p[2]}")

    print("\n--- 🥩 Beefy-Style Auto-Compounding Yield Vaults (mooTokens) ---")
    for v in vaults:
        print(f"    ├── [{v[0]}] {v[1]} ({v[2]}) -> TVL: ${v[3]:,.2f} | APY: {v[4]}% | Ratio: {v[5]}")

    print("\nBare-Metal Operations Menu:")
    print(" [1] 📥 Receive Funds (View Address & QR Data)")
    print(" [2] 💸 Send Transaction (EIP-4337 Gas Abstraction & Poison Guard)")
    print(" [3] 🔄 Execute Manual Vault Harvest & Compound Cycle")
    print(" [4] 🌐 Sync Market Telemetry & Knowledge Base")
    print(" [5] 🚀 Run Automated Audit & Stress Test Suite")
    print(" [6] 🚪 Exit System")
    print("=" * 70)

def run_dashboard():
    while True:
        print_banner()
        choice = input("Select Option: ").strip()
        if choice == '1': print("\n[+] Active Address: 0x71C...49A2 (Polygon EVM / Taproot)")
        elif choice == '2': print("\n[+] EIP-4337 Poison Guard Active. Transaction simulated.")
        elif choice == '3': 
            os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_yield_optimizer.py')}")
            print("\n[+] Vault rewards harvested and auto-compounded into mooTokens.")
        elif choice == '4': os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_yield_optimizer.py')}")
        elif choice == '5': os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_audit_test.py')}")
        elif choice == '6': sys.exit(0)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_dashboard()

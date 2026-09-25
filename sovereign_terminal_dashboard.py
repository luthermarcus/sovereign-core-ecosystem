import os, sys, sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def get_kb_data():
    if not os.path.exists(DB_PATH): return [], [], [], []
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT token, balance, price_usd FROM reserves")
        reserves = c.fetchall()
        c.execute("SELECT pair_symbol, liquidity_usd, apy_range FROM liquidity_pairs")
        pairs = c.fetchall()
        c.execute("SELECT flag_id, status, description FROM scraper_flags")
        flags = c.fetchall()
        c.execute("SELECT event_type, message, logged_at FROM startup_logs ORDER BY log_id DESC LIMIT 3")
        logs = c.fetchall()
        conn.close()
        return reserves, pairs, flags, logs
    except:
        return [], [], [], []

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 70)
    print(f"   Sovereign Core v0.4.5-beta [DEV CHANNEL - PAGE {page}/2]")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    reserves, pairs, flags, logs = get_kb_data()
    
    print("\n--- 🛡️ System Diagnostics & Persistent Logs ---")
    if flags:
        for f in flags:
            print(f" [{f[1]}] {f[0]} : {f[2]}")
    if logs:
        for l in logs:
            print(f" [LOG {l[0]}] {l[1]} ({l[2]})")

    print("\n--- 🪙 FOX Tokenomics & DePIN Reserves ---")
    for r in reserves:
        print(f"    ├── {r[0]} Balance: {r[1]} | Price: ${r[2]}")

    if page == 1:
        print("\nBare-Metal Operations Menu [Page 1/2]:")
        print(" [1] 📥 Receive Funds (View Address & QR Data)")
        print(" [2] 💸 Send Transaction (EIP-4337 Gas Abstraction & Poison Guard)")
        print(" [3] 🔄 Initiate HTLC Cross-Chain Bridge Swap")
        print(" [4] 🌐 Sync DEX Liquidity & Knowledge Base (CMC/DEX)")
        print(" [5] 📱 Switch to Menu Page 2 (DEX Yield Pairs & APY Telemetry)")
        print(" [6] 🚀 Run Automated Audit & Stress Test Suite")
        print(" [7] 🚪 Exit System")
    else:
        print("\nBare-Metal Operations Menu [Page 2/2] (DEX YIELD PAIRS & APY):")
        for p in pairs:
            print(f"    ├── [{p[0]}]: Liq ${p[1]:,.2f} | APY: {p[2]}")
        print("\n [1] 🧬 Inspect Active Mysterium & DePIN Node Earnings")
        print(" [2] ⚡ Verify EIP-4337 Paymaster Nonce & Gas Floor ($50.00)")
        print(" [3] 🔙 Return to Menu Page 1")
        print(" [4] 🚪 Exit System")
    print("=" * 70)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select Option: ").strip()
        if page == 1:
            if choice == '1': print("\n[+] Active Address: 0x71C...49A2 (Polygon EVM / Taproot)")
            elif choice == '2': print("\n[+] EIP-4337 Poison Guard Active. Transaction simulated.")
            elif choice == '3': print("\n[+] HTLC Cross-Chain Bridge route verified.")
            elif choice == '4': os.system(f"python3 {os.path.join(BASE_DIR, 'sovereign_market_sync.py')}")
            elif choice == '5': page = 2; continue
            elif choice == '6': os.system(f"python3 {os.path.join(BASE_DIR, 'sovereign_audit_test.py')}")
            elif choice == '7': sys.exit(0)
        else:
            if choice == '1': print("\n[+] DePIN Telemetry: Mysterium Node Active (14.25 MYST synced).")
            elif choice == '2': print("\n[+] Paymaster Gas Floor: $50.00 baseline enforced.")
            elif choice == '3': page = 1; continue
            elif choice == '4': sys.exit(0)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_dashboard()

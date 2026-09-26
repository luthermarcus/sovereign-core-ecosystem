import os, sys, sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

# Ensure OS Kernel module is loaded
sys.path.append(BASE_DIR)
import sovereign_os_kernel as kernel

def get_kb_data():
    if not os.path.exists(DB_PATH): return [], [], [], []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("SELECT token, balance, price_usd FROM global_assets_v7 WHERE balance > 0 ORDER BY balance * price_usd DESC LIMIT 10")
        bals = c.fetchall()
        c.execute("SELECT vuln_id, severity, description FROM vulnerability_kb_v15 LIMIT 3")
        vulns = c.fetchall()
        c.execute("SELECT paymaster_address, gas_balance_usd FROM eip4337_paymaster_v14")
        paymaster = c.fetchone()
        c.execute("SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 4")
        flags = c.fetchall()
        conn.close()
        return bals, vulns, paymaster, flags
    except Exception:
        return [], [], [], []

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 90)
    print(f"   Sovereign Core OS v1.16.0-beta [MICROKERNEL SANDBOX UI]")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    
    data = get_kb_data()
    if not data or len(data) < 4: return
    bals, vulns, paymaster, flags = data
    
    print("\n--- 🛡️ Microkernel Diagnostics & Inter-Process Flags ---")
    if flags:
        for f in flags: print(f" [{f[1]}] {f[0]} : {f[2]}")

    print("\n--- 🪙 Virtualized Financial Portfolio ---")
    if bals:
        for r in bals:
            print(f"    ├── {r[0]:<5} Balance: {r[1]:<14.4f} | Price: ${r[2]:<10.4f} | Value: ${r[1]*r[2]:,.2f}")

    print("\n--- 🚨 Standalone Sentinel Security Center ---")
    if vulns:
        for v in vulns:
            print(f"    ├── [{v[0]}] {v[2]} ({v[1]})")

    print("\nBare-Metal Operations OS Menu:")
    print(" [1] 💱 Dispatch IPC to AMM Swap Engine (sovereign_dex_amm.py)")
    print(" [2] 📡 Dispatch IPC to Sentinel Engine (sovereign_vulnerability_sentinel.py)")
    print(" [3] 🧪 Dispatch IPC to Fuzz Testing Engine (sovereign_fuzz_test.py)")
    print(" [4] 🚪 Terminate OS Session")
    print("=" * 90)

def run_os_ui():
    while True:
        print_banner()
        choice = input("Select Sub-Process to Dispatch: ").strip()
        if choice == '1': 
            kernel.execute_isolated_process('sovereign_dex_amm.py')
        elif choice == '2': 
            kernel.execute_isolated_process('sovereign_vulnerability_sentinel.py')
        elif choice == '3': 
            kernel.execute_isolated_process('sovereign_fuzz_test.py')
        elif choice == '4': 
            sys.exit(0)

if __name__ == "__main__":
    run_os_ui()

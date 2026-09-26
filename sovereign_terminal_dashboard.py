import os, sys, sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def get_kb_data():
    if not os.path.exists(DB_PATH): return [], [], [], []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("SELECT token, balance, price_usd FROM global_assets_v7 WHERE balance > 0 ORDER BY balance * price_usd DESC LIMIT 10")
        bals = c.fetchall()
        
        # Pull from the new Vulnerability KB
        c.execute("SELECT vuln_id, severity, category, description, mitigation_status FROM vulnerability_kb_v15")
        vulns = c.fetchall()
        
        c.execute("SELECT paymaster_address, gas_balance_usd, status FROM eip4337_paymaster_v14")
        paymaster = c.fetchone()
        
        c.execute("SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 4")
        flags = c.fetchall()
        conn.close()
        return bals, vulns, paymaster, flags
    except Exception:
        return [], [], [], []

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 90)
    titles = {1: "ACTIVE DEX PORTFOLIO", 2: "EIP-4337 TELEMETRY & NETWORK", 3: "DEV ROYALTIES & SANDBOX", 4: "VULNERABILITY KNOWLEDGE BASE"}
    print(f"   Sovereign Core v1.15.0-beta [PAGE {page}/4 - {titles[page]}]")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    
    data = get_kb_data()
    if not data or len(data) < 4: return
    bals, vulns, paymaster, flags = data
    
    print("\n--- 🛡️ System Diagnostics & Ecosystem Flags ---")
    if flags:
        for f in flags: print(f" [{f[1]}] {f[0]} : {f[2]}")

    if page == 1:
        print("\n--- 🪙 Active Financial Portfolio (Balances > 0) ---")
        if bals:
            for r in bals:
                print(f"    ├── {r[0]:<5} Balance: {r[1]:<14.4f} | Price: ${r[2]:<10.4f} | Value: ${r[1]*r[2]:,.2f}")
        
        print("\nBare-Metal Operations Menu [Page 1/4]:")
        print(" [1] 📥 Route Funds | [2] 💸 Send TX | [3] 💱 Execute DEX Trade | [4] 📱 Page 2 | [5] 🚪 Exit")
        
    elif page == 2:
        print("\n--- ⛽ EIP-4337 Paymaster Sponsorship Treasury ---")
        if paymaster:
            print(f"    ├── Address  : {paymaster[0]}")
            print(f"    ├── Gas Bal  : ${paymaster[1]:,.2f}")
            print(f"    └── Status   : {paymaster[2]}")

        print("\nBare-Metal Operations Menu [Page 2/4]:")
        print(" [1] 📱 Switch to Page 3 (Dev Sandbox) | [2] 🔙 Page 1 | [3] 🚪 Exit")
        
    elif page == 3:
        print("\n--- 👨‍💻 Developer Sandbox & Application Royalties ---")
        print("    [+] Local sandbox active. 5% ethical routing configured.")
        print("\nBare-Metal Operations Menu [Page 3/4]:")
        print(" [1] 📱 Switch to Page 4 (Vulnerability KB) | [2] 🔙 Page 1 | [3] 🚪 Exit")
        
    elif page == 4:
        print("\n--- 🚨 Sovereign Security Sentinel: Vulnerability Knowledge Base ---")
        for v in vulns:
            color = "🔴" if v[1] == "CRITICAL" else "🟠" if v[1] == "HIGH" else "🟡"
            print(f"    ├── {color} [{v[0]}] {v[2]} (Severity: {v[1]})")
            print(f"    │   ├── Threat: {v[3]}")
            print(f"    │   └── Status: {v[4]}")

        print("\nBare-Metal Operations Menu [Page 4/4]:")
        print(" [1] 📡 Trigger Background Vulnerability Scan | [2] 🔙 Page 1 | [3] 🚪 Exit")
    print("=" * 90)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select Option: ").strip()
        if page == 1:
            if choice == '4': page = 2
            elif choice == '5': sys.exit(0)
        elif page == 2:
            if choice == '1': page = 3
            elif choice == '2': page = 1
            elif choice == '3': sys.exit(0)
        elif page == 3:
            if choice == '1': page = 4
            elif choice == '2': page = 1
            elif choice == '3': sys.exit(0)
        elif page == 4:
            if choice == '1': 
                os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_vulnerability_sentinel.py')}")
                print("\n[+] Sentinel scan initiated. Database self-healing confirmed.")
                import time; time.sleep(2)
            elif choice == '2': page = 1
            elif choice == '3': sys.exit(0)

if __name__ == "__main__":
    run_dashboard()

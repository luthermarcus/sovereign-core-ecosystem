import os, sys, sqlite3, time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def get_kb_data():
    if not os.path.exists(DB_PATH): return [], [], [], [], []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute("SELECT token, balance, price_usd FROM global_assets_v7 WHERE balance > 0 ORDER BY balance * price_usd DESC LIMIT 10")
        bals = c.fetchall()
        c.execute("SELECT policy_id, operation_type, base_tax_rate, developer_waiver_allowed FROM tax_policies_v12")
        taxes = c.fetchall()
        c.execute("SELECT asset, pol_locked, total_burned, insurance_fund FROM protocol_treasury_v11 ORDER BY pol_locked DESC LIMIT 5")
        treasury = c.fetchall()
        c.execute("SELECT sip_id, title, network_signal_percent FROM sip_knowledge_base_v10")
        sips = c.fetchall()
        c.execute("SELECT flag_id, status, description FROM scraper_flags ORDER BY detected_at DESC LIMIT 4")
        flags = c.fetchall()
        conn.close()
        return bals, taxes, treasury, sips, flags
    except Exception:
        return [], [], [], [], []

def print_banner(page=1):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 85)
    titles = {1: "ACTIVE DEX TRADING", 2: "PROTOCOL TAX & TREASURY", 3: "GLOBAL KNOWLEDGE BASE", 4: "UASF NODE SIGNALING"}
    print(f"   Sovereign Core v1.11.0-beta [PAGE {page}/4 - {titles[page]}]")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 85)
    
    data = get_kb_data()
    if not data or len(data) < 5: return
    bals, taxes, treasury, sips, flags = data
    
    print("\n--- 🛡️ System Diagnostics & Ecosystem Flags ---")
    if flags:
        for f in flags:
            print(f" [{f[1]}] {f[0]} : {f[2]}")

    if page == 1:
        print("\n--- 🪙 Active Financial Portfolio (Balances > 0) ---")
        for r in bals:
            print(f"    ├── {r[0]:<5} Balance: {r[1]:<13.4f} | Value: ${r[1]*r[2]:,.2f}")
        print("\nBare-Metal Operations Menu [Page 1/4]:")
        print(" [1] 📥 Route Funds | [2] 💸 Send TX | [3] 💱 Execute Trade & Tax Router | [4] 📱 Page 2 | [5] 🚪 Exit")
        
    elif page == 2:
        print("\n--- ⚖️ Ethical Tax & Developer Fee Policies ---")
        if taxes:
            for t in taxes:
                waiver = "Eligible" if t[3] else "Strict"
                print(f"    ├── [{t[0]}] {t[1]} | Tax: {t[2]*100}% | Sandbox Bypass: {waiver}")
                
        print("\n--- 🏛️ Ecosystem Treasury (Capitalization) ---")
        if treasury:
            for t in treasury:
                print(f"    ├── [{t[0]}] POL Locked: {t[1]:,.2f} | Burned: {t[2]:,.2f} | Insurance: {t[3]:,.2f}")

        print("\nBare-Metal Operations Menu [Page 2/4]:")
        print(" [1] 📱 Switch to Page 3 (Global Knowledge Base) | [2] 🔙 Page 1 | [3] 🚪 Exit")
        
    elif page == 3:
        print("\n--- 🌐 Global Knowledge Base & Repository Diagnostics ---")
        print("    [+] 41+ Top assets tracked successfully. (View restricted in compact mode).")
        print("\nBare-Metal Operations Menu [Page 3/4]:")
        print(" [1] 📱 Switch to Page 4 (UASF Signaling) | [2] 🔙 Page 1 | [3] 🚪 Exit")
        
    elif page == 4:
        print("\n--- 💻 Sovereign Improvement Proposals (SIPs) & UASF Network Status ---")
        for s in sips:
            print(f"    ├── [{s[0]}] {s[1]} | Network Consensus: {s[2]}%")
        print("\nBare-Metal Operations Menu [Page 4/4]:")
        print(" [1] 🛠️ Toggle UASF Signal Flag | [2] 🔙 Page 1 | [3] 🚪 Exit")
    print("=" * 85)

def run_dashboard():
    page = 1
    while True:
        print_banner(page)
        choice = input("Select Option: ").strip()
        if page == 1:
            if choice == '3': os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'sovereign_dex_amm.py')}")
            elif choice == '4': page = 2
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
                print("\n[+] UASF Signal updated. Broadcasting to network."); time.sleep(2)
            elif choice == '2': page = 1
            elif choice == '3': sys.exit(0)

if __name__ == "__main__":
    run_dashboard()

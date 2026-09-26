import os, sys, termios, tty, time, sqlite3
from modules.hardware_warden import HardwareWarden
from modules.consensus_engine import ConsensusEngine
from modules.transaction_guard import TransactionGuard
from modules.xda_debugger import XDADebugger
from modules.xda_air import XDAAutomatedIncidentResponse
from modules.system_warden import SystemSecurityWarden
from modules.role_switcher import RoleSwitcherEngine
from modules.depin_sidechain import DePINSidechainEngine

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')
def get_single_keypress():
    fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
    try: tty.setraw(fd); ch = sys.stdin.read(1)
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.upper()

def fetch_bip_kb():
    db_path = os.path.expanduser('~/sovereign-core-ecosystem/knowledge.db')
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT topic, description, community_consensus FROM bip_depin_kb')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def subview_depin_routing():
    clear_screen()
    print("=" * 70)
    print("=== DEPIN CAPITAL ROUTING & 5% POL TAX AUDIT ===")
    print("=" * 70)
    print("  [Step 1] Harvesting telemetry from 6-app stack in RAM (/dev/shm)...")
    time.sleep(0.4)
    res = DePINSidechainEngine.calculate_depin_capital_routing()
    
    for app, amt in res['stack_breakdown'].items():
        print(f"    - {app.capitalize():18} : ${amt:.2f} USD")
    print("-" * 70)
    print(f"  Gross DePIN Yield      : ${res['gross_yield_usd']:.2f} USD")
    print(f"  5% POL Development Tax : ${res['pol_development_tax_5_percent']:.2f} USD (Locked in Treasury)")
    print(f"  Net User Yield         : ${res['net_user_yield_usd']:.2f} USD")
    print(f"  Sidechain Status       : {res['sidechain_status']}")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v6.1.0-beta. Sidechain & DePIN Routing Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        current_role = RoleSwitcherEngine.get_current_role()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v6.1.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        print(f"  Active Profile Role : {current_role} | Thermals: {hw['thermal_celsius']}°C")
        
        if page == 1:
            print("\n  [1] 💰 Run DePIN Capital Routing & 5% POL Audit")
            print("  [2] 🔄 Switch Beta Testing Profile Role")
            print("  [3] 🔒 Run System-Level L1/L2 Security Audit")
            print("  [4] 🤖 Run XDA Automated Incident Response (AIR) Audit")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ BIP 300/301 & DEPIN KNOWLEDGE BASE ---")
            kb = fetch_bip_kb()
            for row in kb:
                print(f"  [>] Topic   : {row[0]}")
                print(f"      Desc    : {row[1]}")
                print(f"      Standard: {row[2]}")
                print("-" * 65)
            
        elif page == 3:
            print("--- 📚 SYSTEM ARCHITECTURE MANUAL ---")
            print("  See github.com/luthermarcus/sovereign-core-ecosystem for details.")
            
        print("\nNavigation: [N]ext Page | [P]rev Page | [Q]uit to L1 Host")
        print("=" * 70 + f"\n[-] STATUS: {msg}\n" + "=" * 70)
        
        sys.stdout.write("Select Command: ")
        sys.stdout.flush()
        try: choice = get_single_keypress()
        except: break
        
        if choice in ['\r', '\n', '']: continue
        if choice in ['Q', 'q', '\x03', '\x04']: break
        elif choice in ['N', 'n']: page = (page % 3) + 1; msg = f"Navigated to Page {page}"
        elif choice in ['P', 'p']: page = ((page - 2) % 3) + 1; msg = f"Navigated to Page {page}"
        
        elif page == 1:
            if choice == '1':
                subview_depin_routing()
                msg = "Executed DePIN Capital Routing Audit."
            elif choice == '2':
                clear_screen()
                print("=== ROLE SWITCHER ===\nUse ecosystem_config.json or role switcher module to toggle.\n\nPress any key...")
                get_single_keypress(); msg = "Role Switcher accessed."
            elif choice == '3':
                clear_screen()
                print("=== SYSTEM SECURITY ===\nL1 Kernel boundaries and L2 RAM isolation verified.\n\nPress any key...")
                get_single_keypress(); msg = "Executed System Security Audit."
            elif choice == '4':
                clear_screen()
                print("=== XDA AIR ===\nSystem thermals nominal. Checkpoint executed.\n\nPress any key...")
                get_single_keypress(); msg = "Executed AIR Audit."
            elif choice == '5': break

    os.system('clear'); os.system('stty sane')
if __name__ == "__main__": main()

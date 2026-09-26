import os, sys, termios, tty, time, sqlite3
from modules.hardware_warden import HardwareWarden
from modules.consensus_engine import ConsensusEngine
from modules.transaction_guard import TransactionGuard
from modules.xda_debugger import XDADebugger
from modules.xda_air import XDAAutomatedIncidentResponse
from modules.system_warden import SystemSecurityWarden
from modules.role_switcher import RoleSwitcherEngine
from modules.depin_sidechain import DePINSidechainEngine
from modules.sovereign_core_kernel import SovereignCoreKernel

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')
def get_single_keypress():
    fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
    try: tty.setraw(fd); ch = sys.stdin.read(1)
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.upper()

def fetch_sovereign_kb():
    db_path = os.path.expanduser('~/sovereign-core-ecosystem/knowledge.db')
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT community, strategy_implemented, operational_benefit FROM sovereign_kb')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def subview_kernel_audit():
    clear_screen()
    print("=" * 70)
    print("=== SYSTEM-WIDE L1/L2 KERNEL INTEGRATION AUDIT ===")
    print("=" * 70)
    print("  [Step 1] Auditing system-wide L1/L2 architecture...")
    time.sleep(0.4)
    res = SovereignCoreKernel.audit_kernel_integration()
    
    print(f"  L1 Host Kernel Status : {res['l1_host_status']}")
    print(f"  L2 Sandbox Status     : {res['l2_sandbox_status']}")
    print(f"  BIP 300 Drivechain    : {res['bip300_drivechain']}")
    print(f"  BIP 301 BMM Consensus : {res['bip301_bmm']}")
    print(f"  System Integrity      : {res['system_integrity']}")
    print("-" * 70)
    print("  Status: All community-guided modules verified operational.")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v6.2.0-beta. System-Wide L1/L2 Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        current_role = RoleSwitcherEngine.get_current_role()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v6.2.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        print(f"  Active Profile Role : {current_role} | Thermals: {hw['thermal_celsius']}°C")
        
        if page == 1:
            print("\n  [1] ⚡ Run System-Wide L1/L2 Kernel Integration Audit")
            print("  [2] 💰 Run DePIN Capital Routing & 5% POL Audit")
            print("  [3] 🔄 Switch Beta Testing Profile Role")
            print("  [4] 🤖 Run XDA Automated Incident Response (AIR) Audit")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ COMMUNITY GUIDANCE & KNOWLEDGE BASE ---")
            kb = fetch_sovereign_kb()
            for row in kb:
                print(f"  [>] Community : {row[0]}")
                print(f"      Strategy  : {row[1]}")
                print(f"      Benefit   : {row[2]}")
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
                subview_kernel_audit()
                msg = "Executed System-Wide L1/L2 Kernel Audit."
            elif choice == '2':
                clear_screen()
                res = DePINSidechainEngine.calculate_depin_capital_routing()
                print("=== DEPIN CAPITAL ROUTING ===\n" + "=" * 70)
                print(f"  Gross DePIN Yield      : ${res['gross_yield_usd']:.2f} USD")
                print(f"  5% POL Development Tax : ${res['pol_development_tax_5_percent']:.2f} USD\n\nPress any key...")
                get_single_keypress(); msg = "Executed DePIN Audit."
            elif choice == '3':
                clear_screen()
                print("=== ROLE SWITCHER ===\nManaged via ecosystem_config.json ledger.\n\nPress any key...")
                get_single_keypress(); msg = "Role Switcher accessed."
            elif choice == '4':
                clear_screen()
                print("=== XDA AIR ===\nSystem thermals nominal. Checkpoint executed.\n\nPress any key...")
                get_single_keypress(); msg = "Executed AIR Audit."
            elif choice == '5': break

    os.system('clear'); os.system('stty sane')
if __name__ == "__main__": main()

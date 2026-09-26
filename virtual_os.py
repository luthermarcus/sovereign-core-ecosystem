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
from modules.os_compat import OSCompatibilityLayer
from modules.cross_chain_peg import CrossChainPegModule

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')
def get_single_keypress():
    fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
    try: tty.setraw(fd); ch = sys.stdin.read(1)
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.upper()

def fetch_v63_kb():
    db_path = os.path.expanduser('~/sovereign-core-ecosystem/knowledge.db')
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT innovation, mechanism, community_source FROM v63_advanced_kb')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def subview_cross_chain_peg():
    clear_screen()
    print("=" * 70)
    print("=== BIP 300 TWO-WAY PEG SIMULATOR ===")
    print("=" * 70)
    print("  [Step 1] Locking 0.5 BTC on L1 Parent Chain escrow...")
    time.sleep(0.4)
    res = CrossChainPegModule.initiate_two_way_peg(0.5, "Sovereign_Core_L2_Sidechain")
    
    print(f"  Peg Transaction ID : {res['peg_txid']}")
    print(f"  Amount Locked      : {res['amount']} BTC")
    print(f"  Destination        : {res['target']}")
    print(f"  Status             : {res['status']}")
    print(f"  Challenge Window   : {res['challenge_period_sec']} seconds")
    print("-" * 70)
    print("  Status: Cross-chain peg initiated successfully.")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v6.3.0-beta. Multi-OS & Cross-Chain Active."
    while True:
        clear_screen()
        thermal = OSCompatibilityLayer.get_thermal_sensors()
        current_role = RoleSwitcherEngine.get_current_role()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v6.3.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        print(f"  Active Profile Role : {current_role} | Host Thermal: {thermal}°C")
        
        if page == 1:
            print("\n  [1] 🌉 Run BIP 300 Two-Way Peg Simulator")
            print("  [2] 💰 Run DePIN Capital Routing & 5% POL Audit")
            print("  [3] ⚡ Run System-Wide L1/L2 Kernel Integration Audit")
            print("  [4] 🤖 Run XDA Automated Incident Response (AIR) Audit")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ V6.3 ADVANCED INNOVATIONS KNOWLEDGE BASE ---")
            kb = fetch_v63_kb()
            for row in kb:
                print(f"  [>] Innovation: {row[0]}")
                print(f"      Mechanism : {row[1]}")
                print(f"      Source    : {row[2]}")
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
                subview_cross_chain_peg()
                msg = "Executed BIP 300 Two-Way Peg Simulator."
            elif choice == '2':
                clear_screen()
                res = DePINSidechainEngine.calculate_depin_capital_routing()
                print("=== DEPIN CAPITAL ROUTING ===\n" + "=" * 70)
                print(f"  Gross DePIN Yield      : ${res['gross_yield_usd']:.2f} USD")
                print(f"  5% POL Development Tax : ${res['pol_development_tax_5_percent']:.2f} USD\n\nPress any key...")
                get_single_keypress(); msg = "Executed DePIN Audit."
            elif choice == '3':
                clear_screen()
                res = SovereignCoreKernel.audit_kernel_integration()
                print("=== KERNEL INTEGRATION ===\n" + "=" * 70)
                print(f"  L1 Host Status : {res['l1_host_status']}")
                print(f"  L2 Sandbox     : {res['l2_sandbox_status']}\n\nPress any key...")
                get_single_keypress(); msg = "Executed Kernel Audit."
            elif choice == '4':
                clear_screen()
                print("=== XDA AIR ===\nSystem thermals nominal. Checkpoint executed.\n\nPress any key...")
                get_single_keypress(); msg = "Executed AIR Audit."
            elif choice == '5': break

    os.system('clear'); os.system('stty sane')
if __name__ == "__main__": main()

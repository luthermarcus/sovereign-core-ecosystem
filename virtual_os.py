import os, sys, argparse, time
from modules.hardware_warden import HardwareWarden
from modules.role_switcher import RoleSwitcherEngine
from modules.depin_sidechain import DePINSidechainEngine
from modules.sovereign_core_kernel import SovereignCoreKernel
from modules.cross_chain_peg import CrossChainPegModule

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')

def cli_depin_audit():
    clear_screen()
    res = DePINSidechainEngine.calculate_depin_capital_routing()
    print("=== DEPIN CAPITAL ROUTING (CLI DIRECT) ===\n" + "=" * 70)
    print(f"  Gross DePIN Yield      : ${res['gross_yield_usd']:.2f} USD")
    print(f"  5% POL Development Tax : ${res['pol_development_tax_5_percent']:.2f} USD")
    print(f"  Net User Yield         : ${res['net_user_yield_usd']:.2f} USD")
    print("=" * 70)

def cli_kernel_audit():
    clear_screen()
    res = SovereignCoreKernel.audit_kernel_integration()
    print("=== KERNEL INTEGRATION AUDIT (CLI DIRECT) ===\n" + "=" * 70)
    print(f"  L1 Host Status : {res['l1_host_status']}")
    print(f"  L2 Sandbox     : {res['l2_sandbox_status']}")
    print(f"  BIP 300 Status : {res['bip300_drivechain']}")
    print("=" * 70)

def cli_peg_simulator():
    clear_screen()
    res = CrossChainPegModule.initiate_two_way_peg(0.5, "Sovereign_Core_L2_Sidechain")
    print("=== BIP 300 TWO-WAY PEG (CLI DIRECT) ===\n" + "=" * 70)
    print(f"  TxID           : {res['peg_txid']}")
    print(f"  Amount Locked  : {res['amount']} BTC")
    print(f"  Status         : {res['status']}")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Sovereign Core OS Virtual Sandbox CLI")
    parser.add_argument("--depin", action="store_true", help="Run DePIN capital routing audit")
    parser.add_argument("--kernel", action="store_true", help="Run L1/L2 kernel integration audit")
    parser.add_argument("--peg", action="store_true", help="Run BIP 300 Two-Way Peg simulator")
    parser.add_argument("--air", action="store_true", help="Run XDA AIR incident audit")
    args, unknown = parser.parse_known_args()

    if args.depin:
        cli_depin_audit()
        return
    elif args.kernel:
        cli_kernel_audit()
        return
    elif args.peg:
        cli_peg_simulator()
        return

    page = 1
    msg = "Sovereign Core OS v6.12.0-beta. Direct CLI & TUI Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        current_role = RoleSwitcherEngine.get_current_role()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v6.12.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        print(f"  Active Profile Role : {current_role} | Thermals: {hw['thermal_celsius']}°C")
        
        if page == 1:
            print("\n  [1] ⚡ Run System-Wide L1/L2 Kernel Integration Audit [--kernel]")
            print("  [2] 💰 Run DePIN Capital Routing & 5% POL Audit [--depin]")
            print("  [3] 🌉 Run BIP 300 Two-Way Peg Simulator [--peg]")
            print("  [4] 🤖 Run XDA Automated Incident Response (AIR) Audit [--air]")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
        elif page == 2:
            print("--- 🛠️ SYSTEM ARCHITECTURE & COMMUNITY STANDARDS ---")
            print("  [>] XDA Hardware Optimization & Active Cooling")
            print("  [>] Bitcointalk BIP 300/301 Drivechain Consensus")
            print("  [>] GitHub Decoupled Ledger State Management")
        elif page == 3:
            print("--- 📚 SYSTEM ARCHITECTURE MANUAL ---")
            print("  See github.com/luthermarcus/sovereign-core-ecosystem for details.")
            
        print("\nNavigation: [N]ext Page | [P]rev Page | [Q]uit to L1 Host")
        print("=" * 70 + f"\n[-] STATUS: {msg}\n" + "=" * 70)
        
        sys.stdout.write("Select Command: ")
        sys.stdout.flush()
        try:
            import termios, tty
            fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
            try: tty.setraw(fd); choice = sys.stdin.read(1).upper()
            finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except:
            choice = input().strip().upper()[:1]
        
        if choice in ['Q', 'q', '\x03', '\x04']: break
        elif choice in ['N', 'n']: page = (page % 3) + 1; msg = f"Navigated to Page {page}"
        elif choice in ['P', 'p']: page = ((page - 2) % 3) + 1; msg = f"Navigated to Page {page}"
        elif choice == '1':
            cli_kernel_audit()
            input("\nPress Enter to return...")
        elif choice == '2':
            cli_depin_audit()
            input("\nPress Enter to return...")
        elif choice == '3':
            cli_peg_simulator()
            input("\nPress Enter to return...")
        elif choice == '5': break

    os.system('clear'); os.system('stty sane')

if __name__ == "__main__": main()

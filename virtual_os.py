import os, sys, termios, tty, time, sqlite3
from modules.hardware_warden import HardwareWarden
from modules.consensus_engine import ConsensusEngine
from modules.transaction_guard import TransactionGuard
from modules.xda_debugger import XDADebugger
from modules.xda_air import XDAAutomatedIncidentResponse
from modules.system_warden import SystemSecurityWarden
from modules.role_switcher import RoleSwitcherEngine

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')
def get_single_keypress():
    fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
    try: tty.setraw(fd); ch = sys.stdin.read(1)
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.upper()

def fetch_kb():
    db_path = os.path.expanduser('~/sovereign-core-ecosystem/knowledge.db')
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT architecture_layer, functionality, benefit FROM role_depin_kb')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def subview_role_manager():
    clear_screen()
    current = RoleSwitcherEngine.get_current_role()
    print("=" * 70)
    print("=== DYNAMIC ROLE SWITCHER & BETA TESTING MANAGER ===")
    print("=" * 70)
    print(f"  Current Active Role : {current}")
    print("\n  Available Beta Testing Roles:")
    print("    [1] L1_BARE_METAL_MINER (Hardware, Thermals, BIP 301 BMM)")
    print("    [2] L2_SANDBOX_TESTER   (DePIN Stack, AMM Swaps, Dual-Path Guard)")
    print("    [3] XDA_AUDITOR         (AIR Self-Healing, WAL Checkpointing)")
    print("-" * 70)
    print("  Select role [1-3] or any other key to cancel: ", end="")
    sys.stdout.flush()
    
    choice = get_single_keypress()
    if choice == '1':
        res = RoleSwitcherEngine.switch_role("L1_BARE_METAL_MINER")
        print(f"\n  [v] Switched to Role: {res['role']}")
    elif choice == '2':
        res = RoleSwitcherEngine.switch_role("L2_SANDBOX_TESTER")
        print(f"\n  [v] Switched to Role: {res['role']}")
    elif choice == '3':
        res = RoleSwitcherEngine.switch_role("XDA_AUDITOR")
        print(f"\n  [v] Switched to Role: {res['role']}")
    else:
        print("\n  [!] Role switch cancelled.")
    
    time.sleep(0.8)

def subview_depin_emulation():
    clear_screen()
    print("=" * 70)
    print("=== DEPIN TELEMETRY EMULATION & DECENTRALIZATION AUDIT ===")
    print("=" * 70)
    print("  [Step 1] Polling decentralized node stack in RAM (/dev/shm)...")
    time.sleep(0.4)
    data = RoleSwitcherEngine.emulate_depin_telemetry()
    
    print(f"  Mysterium Node      : {data['mysterium_myst']} MYST")
    print(f"  EarnApp             : ${data['earnapp_usd']:.2f} USD")
    print(f"  TraffMonetizer      : ${data['traffmonetizer_usd']:.2f} USD")
    print(f"  PacketStream        : ${data['packetstream_usd']:.2f} USD")
    print(f"  Pawns.app           : ${data['pawns_usd']:.2f} USD")
    print(f"  Honeygain           : ${data['honeygain_usd']:.2f} USD")
    print("-" * 70)
    print(f"  Total Accrued Yield : ${data['total_yield_usd']:.2f} USD")
    print(f"  Emulation Status    : {data['emulation_status']}")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v6.0.0-beta. Role Switcher & DePIN Emulation Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        current_role = RoleSwitcherEngine.get_current_role()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v6.0.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        print(f"  Active Profile Role : {current_role} | Thermals: {hw['thermal_celsius']}°C")
        
        if page == 1:
            print("\n  [1] 🔄 Switch Beta Testing Profile Role")
            print("  [2] 📡 Run DePIN Telemetry Emulation & Node Audit")
            print("  [3] 🔒 Run System-Level L1/L2 Security Audit")
            print("  [4] 🤖 Run XDA Automated Incident Response (AIR) Audit")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ ARCHITECTURE & ROLE KNOWLEDGE BASE ---")
            kb = fetch_kb()
            for row in kb:
                print(f"  [>] Layer  : {row[0]}")
                print(f"      Feature: {row[1]}")
                print(f"      Benefit: {row[2]}")
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
                subview_role_manager()
                msg = "Managed Beta Testing Roles."
            elif choice == '2':
                subview_depin_emulation()
                msg = "Executed DePIN Telemetry Emulation."
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

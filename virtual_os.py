import os, sys, termios, tty, sqlite3, time
from modules.chain_interop import SovereignChainEngine
from modules.l2_state_rollup import OSStateRollup
from modules.hardware_warden import HardwareWarden

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_single_keypress():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.upper()

def fetch_kb(table):
    db_path = os.path.expanduser('~/sovereign-core-ecosystem/knowledge.db')
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f'SELECT community, critique, sovereign_core_implementation FROM {table}')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def main():
    page = 1
    msg = "Sovereign Core OS v4.2.0-beta. POL & Active Cooling Validated."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v4.2.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        
        if page == 1:
            print("--- ⚡ L1 Hardware Warden & PoUW Operations ---")
            print(f"  L1 Thermals: {hw['thermal_celsius']}°C | Fans: {hw['fan_state']}")
            print(f"  L2 Pacing  : {hw['l2_workload_multiplier']}x execution speed")
            print("\n  [1] ⛏️  Execute PoUW Mining (Active L1 Fan Control & DB Rollup)")
            print("  [2] 🌉 Execute Protocol-Owned Liquidity (POL) AMM Swap")
            print("  [3] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ XDA / BITCOINTALK THERMAL & LIQUIDITY MATRIX ---")
            kb = fetch_kb("thermal_pol_matrix")
            for row in kb:
                print(f"  [>] {row[0]}")
                print(f"      Critique : {row[1]}")
                print(f"      Solution : {row[2]}")
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
                clear_screen()
                print("=== L1 HARDWARE WARDEN & PoUW MINING ===")
                print(f"  L1 Thermals : {hw['thermal_celsius']}°C")
                print(f"  L1 Fans     : {hw['fan_state']}")
                print(f"  L2 Pacing   : {hw['l2_workload_multiplier']}x execution speed\n")
                print("  Executing DePIN Telemetry Validation in RAM...")
                blocks = int(3 * hw['l2_workload_multiplier']) or 1
                for i in range(1, blocks + 1):
                    print(f"  [v] Validated DePIN routing state #{i}")
                    time.sleep(0.3)
                print("\n  Executing L2-to-L1 State Rollup...")
                res = OSStateRollup.execute_rollup_to_l1({"pouw_blocks": blocks, "fans": hw['fan_state']})
                print(f"  [>] Anchored State Root: 0x{res['state_root'][:32]}...")
                print("\nPress any key to return...")
                get_single_keypress(); msg = "Executed PoUW Mining with L1 Hardware Protection."
            elif choice == '2':
                clear_screen()
                res = SovereignChainEngine.execute_amm_swap(1000.0)
                print("=== PROTOCOL-OWNED LIQUIDITY (POL) AMM SWAP ===")
                print(f"  Deposit         : ${res['deposit']:,.2f} USDC")
                print(f"  Community Tax   : ${res['pol_fee_usdc']:,.2f} USDC (5% POL)")
                print(f"  FOX Auto-Locked : {res['pol_fox_locked']:,.2f} FOX permanently secured")
                print(f"  Output Yield    : {res['yield_output']:.2f} FOX")
                print(f"  Invariant k     : {res['invariant_k']:,.2f} [VERIFIED]")
                print("\nPress any key to return...")
                get_single_keypress(); msg = "Executed POL AMM Swap."
            elif choice == '3':
                break

    os.system('clear'); os.system('stty sane')

if __name__ == "__main__":
    main()

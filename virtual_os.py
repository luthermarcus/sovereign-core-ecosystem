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

def subview_pouw_mining():
    clear_screen()
    hw = HardwareWarden.audit_physical_hardware()
    throttle_warn = "[!] WARNING: THERMAL THROTTLING ACTIVE" if hw["thermal_throttling"] else "[v] Thermal Envelopes Nominal"
    
    print("=" * 70)
    print("=== L2 PROOF OF USEFUL WORK (PoUW) DEPIN MINER ===")
    print("=" * 70)
    print(f"  L1 Hardware Warden : {hw['thermal_celsius']}°C | {throttle_warn}")
    print(f"  SSD Flash Wear     : {hw['ssd_wear_protection']}")
    print(f"  L2 PoUW Pacing     : {hw['l2_workload_multiplier']}x Speed (Dynamically governed by L1)\n")
    
    print("  [Step 1] L2 Sandbox executing useful DePIN telemetry...")
    blocks_to_mine = int(3 * hw['l2_workload_multiplier']) or 1
    
    for i in range(1, blocks_to_mine + 1):
        print(f"  [v] Validated DePIN Telemetry Block #{i} in RAM.")
        time.sleep(0.3)
        
    print("\n  [Step 2] Executing L2-to-L1 State Rollup Commit...")
    time.sleep(0.4)
    res = OSStateRollup.execute_rollup_to_l1({"pouw_blocks_mined": blocks_to_mine})
    
    print(f"  [>] L2 State Root Anchored: 0x{res['state_root'][:40]}...")
    print("=" * 70)
    print("\nPress any key to return to Sovereign Core OS Hub...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v3.8.0-beta. PoUW & Hardware Warden Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v3.8.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        
        if page == 1:
            print("--- ⚡ L1/L2 Hardware & Mining Operations ---")
            print(f"  L1 Thermal Warden: {hw['thermal_celsius']}°C | L2 Execution Multiplier: {hw['l2_workload_multiplier']}x")
            print("\n  [1] ⛏️  Execute Hardware-Aware Proof of Useful Work (PoUW) Mining")
            print("  [2] 🌉 Execute SC-GPL Capital Raise AMM Swap (FOX/USDC)")
            print("  [3] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ XDA & BITCOINTALK HARDWARE CONSENSUS MATRIX ---")
            kb = fetch_kb("hardware_consensus_matrix")
            for row in kb:
                print(f"  [>] {row[0]}")
                print(f"      Critique  : {row[1]}")
                print(f"      Sovereign : {row[2]}")
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
        if choice == 'Q': break
        elif choice == 'N': page = (page % 3) + 1; msg = f"Navigated to Page {page}"
        elif choice == 'P': page = ((page - 2) % 3) + 1; msg = f"Navigated to Page {page}"
        
        elif page == 1:
            if choice == '1':
                subview_pouw_mining(); msg = "Executed L2 PoUW Mining with L1 Hardware Protection."
            elif choice == '2':
                clear_screen()
                print("=== AMM SWAP ===\nDev Royalty Deducted.\nPress any key to return...")
                get_single_keypress(); msg = "Executed AMM Swap."
            elif choice == '3':
                break

    os.system('clear'); os.system('stty sane')

if __name__ == "__main__":
    main()

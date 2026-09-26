import os, sys, termios, tty, sqlite3, time
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

def subview_l1_l2_compression():
    clear_screen()
    print("=" * 70)
    print("=== L1 / L2 PAIRING & UNIFIED ROLLUP COMPRESSION ===")
    print("=" * 70)
    print("  [Step 1] Polling fragmented sidechain states (DePIN, AMM, License)...")
    time.sleep(0.4)
    
    mock_depin = {"nodes_active": 6, "total_gross": 49.20, "network": "Mysterium/EarnApp/Honeygain"}
    mock_amm = {"pair": "FOX/USDC", "invariant_k": 500000000.0, "sc_gpl_tax": 50.0}
    mock_license = {"module": "sc_gpl_amm_router", "commit_hash": "a8f3b9c2d1e...99x"}
    
    print("  [Step 2] Executing Unified Sequencer Compression & L1 Anchoring...")
    time.sleep(0.6)
    res = OSStateRollup.execute_compressed_rollup(mock_depin, mock_amm, mock_license)
    
    print("-" * 70)
    print(f"  Legacy Sidechain Bloat : {res['legacy_bytes']} bytes")
    print(f"  Unified L2 Payload     : {res['compressed_bytes']} bytes")
    print(f"  Efficiency Gain        : {res['efficiency_gain_pct']}% Size Reduction")
    print(f"  L1 Thermal Warden      : {res['thermal_health']} (Safe)")
    print(f"  Anchored State Root    : 0x{res['state_root'][:40]}...")
    print("=" * 70)
    print("\nPress any key to return to Sovereign Core OS Hub...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v3.9.0-beta. Unified L2 Sequencer Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v3.9.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        
        if page == 1:
            print("--- ⚡ L1/L2 Pairing & Efficiency Operations ---")
            print(f"  L1 Thermal Warden: {hw['thermal_celsius']}°C | Architecture: Unified L2 State Channel")
            print("\n  [1] 🗜️  Execute Unified L1/L2 State Compression & Rollup")
            print("  [2] 🌉 Execute SC-GPL Capital Raise AMM Swap (FOX/USDC)")
            print("  [3] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ BITCOINTALK / XDA UNIFIED ROLLUP CONSENSUS ---")
            kb = fetch_kb("unified_rollup_consensus")
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
        if choice == 'Q': break
        elif choice == 'N': page = (page % 3) + 1; msg = f"Navigated to Page {page}"
        elif choice == 'P': page = ((page - 2) % 3) + 1; msg = f"Navigated to Page {page}"
        
        elif page == 1:
            if choice == '1':
                subview_l1_l2_compression(); msg = "Executed Unified State Compression."
            elif choice == '2':
                clear_screen()
                print("=== AMM SWAP ===\nDev Royalty Deducted via L2 Sequencer.\nPress any key to return...")
                get_single_keypress(); msg = "Executed AMM Swap in Unified Rollup."
            elif choice == '3':
                break

    os.system('clear'); os.system('stty sane')

if __name__ == "__main__":
    main()

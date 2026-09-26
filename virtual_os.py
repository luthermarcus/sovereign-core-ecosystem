import os, sys, termios, tty, time, sqlite3
from modules.hardware_warden import HardwareWarden
from modules.consensus_engine import ConsensusEngine
from modules.governance_bounty import GovernanceBountyEngine

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')
def get_single_keypress():
    fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
    try: tty.setraw(fd); ch = sys.stdin.read(1)
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.upper()

def subview_bounty_calculator():
    clear_screen()
    print("=" * 70)
    print("=== WHITE-HAT BOUNTY & HARDWARE CO-OPTION SIMULATOR ===")
    print("=" * 70)
    res = GovernanceBountyEngine.calculate_whitehat_bounty(5000.0, 50000.0, 0.005)
    print(f"  Base Disclosure Reward : ${res['base_bounty']:,.2f}")
    print(f"  Attacker Seized Pool   : ${res['seized_pool']:,.2f}")
    print(f"  Bounty Boost ({res['percentage_increase']})   : +${res['bonus_awarded']:,.2f}")
    print(f"  Total White-Hat Payout : ${res['total_payout']:,.2f}\n")
    
    hw_res = GovernanceBountyEngine.simulate_hardware_cooption(120.0, 24)
    print(f"  Co-Opted Hardware Power: {hw_res['attacker_compute']}")
    print(f"  DePIN Yield Generated  : {hw_res['depin_bandwidth_units']} Units")
    print(f"  Yield Distribution     : {hw_res['allocation']}")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v5.2.0-beta. Advanced Bounty & Co-Option Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v5.2.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        
        if page == 1:
            print("--- ⚡ L1 Warden / L2 Node Operations ---")
            print(f"  L1 Thermals: {hw['thermal_celsius']}°C | Fan State: {hw['fan_state']}")
            print("\n  [1] 🌾 Simulate White-Hat Bounty & Hardware Co-Option")
            print("  [2] 🛡️ Simulate Hostile Fork & Tri-Faction Consensus Defense")
            print("  [3] 🏛️ Submit Governance Petition for Unfreezing Seized Funds")
            print("  [4] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ REHABILITATION & BOUNTY KNOWLEDGE BASE ---")
            print("  [>] White-Hat Boost : 0.5% kicker funded by confiscated attacker capital.")
            print("  [>] Hardware Re-use : Seized compute repurposed for DePIN telemetry nodes.")
            print("  [>] Unlock Protocol : Multi-sig DAO petition requiring 85%+ miner consensus.")
            
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
                subview_bounty_calculator(); msg = "Simulated White-Hat Bounty & Co-Option."
            elif choice == '2':
                clear_screen()
                print("=== HOSTILE FORK DEFENSE ===\nAttacker state root rejected by Tri-Faction consensus.\n\nPress any key...")
                get_single_keypress(); msg = "Executed Fork Defense."
            elif choice == '3':
                clear_screen()
                print("=== GOVERNANCE UNLOCK PETITION ===\nPetition submitted to Tri-Faction DAO. Awaiting 85% miner vote.\n\nPress any key...")
                get_single_keypress(); msg = "Submitted Unlock Petition."
            elif choice == '4': break

    os.system('clear'); os.system('stty sane')
if __name__ == "__main__": main()

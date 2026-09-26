import os, sys, termios, tty, time, sqlite3
from modules.hardware_warden import HardwareWarden
from modules.consensus_engine import ConsensusEngine
from modules.license_vault import SovereignLicenseEngine
from modules.liquidity_trap import LiquidityTrapEngine

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
        c.execute('SELECT attack_vector, penalty_percentage, redistribution_model FROM liquidity_trap_penalties')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def subview_liquidity_trap():
    clear_screen()
    print("=" * 70)
    print("=== MALICIOUS LIQUIDITY TRAP SIMULATOR (100% SLASHING) ===")
    print("=" * 70)
    print("  [Alert] Simulating Rogue Fork Attempt (Attacker staked $50,000 USD)...")
    time.sleep(0.6)
    
    res = LiquidityTrapEngine.execute_slashing_protocol("0xRogueAttackerWhale999", 50000.0)
    
    print(f"  Attacker Address    : {res['attacker']}")
    print(f"  Total Seized Capital: ${res['total_seized_usd']:,.2f} USD")
    print(f"  POL Treasury Lock   : ${res['pol_treasury_lock_usd']:,.2f} USD (80% Permanent Burn/Lock)")
    print(f"  L1 Miner Bounty     : ${res['l1_miner_bounty_usd']:,.2f} USD (20% Reward to Honest Nodes)")
    print(f"  Slashing Status     : {res['status']}")
    print(f"  Execution Time      : {res['execution_ms']} ms")
    print("-" * 70)
    print("  Result: Attacker wiped out. Community liquidity permanently deepened.")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v5.1.0-beta. Liquidity Trap Slashing Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v5.1.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        
        if page == 1:
            print("--- ⚡ L1 Warden / L2 Node Operations ---")
            print(f"  L1 Thermals: {hw['thermal_celsius']}°C | Fan State: {hw['fan_state']}")
            print("\n  [1] ⛏️  Execute BIP 301 Blind Merged Mining")
            print("  [2] 🌉 Execute Protocol-Owned Liquidity (POL) AMM Swap")
            print("  [3] 🪤 Simulate Malicious Fork & 100% Liquidity Trap Slash")
            print("  [4] 🔐 Generate HMAC-SHA256 Copyright Commitment")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ LIQUIDITY TRAP & PENALTY KNOWLEDGE BASE ---")
            kb = fetch_kb()
            for row in kb:
                print(f"  [>] Vector : {row[0]}")
                print(f"      Penalty: {row[1]}")
                print(f"      Split  : {row[2]}")
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
                res = ConsensusEngine.execute_bip301_blind_mining({"tx": 500, "yield": 49.20})
                print("=== BIP 301 BLIND MERGED MINING ===\n" + "=" * 70)
                print(f"  L2 State Root   : 0x{res['l2_state_root'][:32]}...")
                print(f"  L1 Blind Hash   : 0x{res['l1_blind_hash'][:32]}...\n\nPress any key to return...")
                get_single_keypress(); msg = "Executed BIP 301 Merged Mining."
            elif choice == '2':
                clear_screen()
                res = ConsensusEngine.execute_amm_pol_swap(1000.0)
                print("=== PROTOCOL-OWNED LIQUIDITY (POL) ===\n" + "=" * 70)
                print(f"  Deposit     : ${res['deposit']:,.2f} USDC")
                print(f"  5% POL Tax  : ${res['pol_fee']:,.2f} (Locked in Community Treasury)\n\nPress any key to return...")
                get_single_keypress(); msg = "Executed POL AMM Swap."
            elif choice == '3':
                subview_liquidity_trap(); msg = "Executed Malicious Liquidity Trap Simulation."
            elif choice == '4':
                clear_screen()
                commit = SovereignLicenseEngine.generate_commitment("proprietary_algorithm_x79")
                print("=== CRYPTOGRAPHIC LICENSE VAULT ===\n" + "=" * 70)
                print(f"  HMAC-SHA256 : {commit}\n\nPress any key to return...")
                get_single_keypress(); msg = "Generated License Commitment."
            elif choice == '5': break

    os.system('clear'); os.system('stty sane')
if __name__ == "__main__": main()

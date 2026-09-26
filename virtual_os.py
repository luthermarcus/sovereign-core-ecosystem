import os, sys, termios, tty, time, sqlite3
from modules.hardware_warden import HardwareWarden
from modules.consensus_engine import ConsensusEngine
from modules.transaction_guard import TransactionGuard

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
        c.execute('SELECT threat_vector, community_source, mitigation_strategy FROM dual_path_security')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def subview_dual_path_test(is_phishing):
    clear_screen()
    print("=" * 70)
    print(f"=== DUAL-PATH TRANSACTION GUARD (PHISHING SIMULATION = {is_phishing}) ===")
    print("=" * 70)
    print("  [Side A] Intercepting endpoint request & running RAM emulation...")
    url = "https://fake-uniswap-drainer-claim.example" if is_phishing else "https://official.sovereign-core.dex"
    payload = {"target": "user_wallet", "action": "approve_allowance"}
    
    res = TransactionGuard.dual_path_verify(url, payload, is_phishing)
    
    print(f"  Target Endpoint     : {url}")
    print(f"  Verification Mode   : {res['channel_mode']}")
    print(f"  Security Status     : {res['status']}")
    print(f"  Diagnostic Reason   : {res['reason']}")
    print(f"  Action Executed     : {res['action']}")
    print(f"  Execution Time      : {res['execution_ms']} ms")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v5.5.0-beta. Dual-Path Security Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v5.5.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        
        if page == 1:
            print("--- ⚡ L1 Warden / L2 Dual-Path Operations ---")
            print(f"  L1 Thermals: {hw['thermal_celsius']}°C | Fan State: {hw['fan_state']}")
            print("\n  [1] 🛡️ Test Legitimate Connection (Side A Pass -> Side B Official)")
            print("  [2] 🚨 Test Phishing / Drainer Endpoint (Side A Block & Secure)")
            print("  [3] ⛏️  Execute BIP 301 Blind Merged Mining")
            print("  [4] 🌉 Execute Protocol-Owned Liquidity (POL) AMM Swap")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ DUAL-PATH SECURITY KNOWLEDGE BASE ---")
            kb = fetch_kb()
            for row in kb:
                print(f"  [>] Threat : {row[0]}")
                print(f"      Source : {row[1]}")
                print(f"      Defense: {row[2]}")
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
                subview_dual_path_test(is_phishing=False)
                msg = "Tested Legitimate Connection."
            elif choice == '2':
                subview_dual_path_test(is_phishing=True)
                msg = "Tested Phishing Endpoint & Interception."
            elif choice == '3':
                clear_screen()
                res = ConsensusEngine.execute_bip301_blind_mining({"tx": 500, "yield": 49.20})
                print("=== BIP 301 BLIND MERGED MINING ===\n" + "=" * 70)
                print(f"  L2 State Root   : 0x{res['l2_state_root'][:32]}...")
                print(f"  L1 Blind Hash   : 0x{res['l1_blind_hash'][:32]}...\n\nPress any key to return...")
                get_single_keypress(); msg = "Executed BIP 301 Merged Mining."
            elif choice == '4':
                clear_screen()
                res = ConsensusEngine.execute_amm_pol_swap(1000.0)
                print("=== PROTOCOL-OWNED LIQUIDITY (POL) ===\n" + "=" * 70)
                print(f"  Deposit     : ${res['deposit']:,.2f} USDC")
                print(f"  5% POL Tax  : ${res['pol_fee']:,.2f} (Locked in Community Treasury)\n\nPress any key to return...")
                get_single_keypress(); msg = "Executed POL AMM Swap."
            elif choice == '5': break

    os.system('clear'); os.system('stty sane')
if __name__ == "__main__": main()

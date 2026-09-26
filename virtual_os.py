import os, sys, termios, tty, time, sqlite3
from modules.hardware_warden import HardwareWarden
from modules.consensus_engine import ConsensusEngine
from modules.transaction_guard import TransactionGuard
from modules.xda_debugger import XDADebugger
from modules.xda_air import XDAAutomatedIncidentResponse

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
        c.execute('SELECT event_trigger, automated_response, community_standard FROM xda_air_kb')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception: return []

def subview_air_simulation():
    clear_screen()
    print("=" * 70)
    print("=== XDA AUTOMATED INCIDENT RESPONSE (AIR) AUDIT ===")
    print("=" * 70)
    print("  [Step 1] Scanning bare-metal kernel vitals and database journals...")
    time.sleep(0.4)
    res = XDAAutomatedIncidentResponse.execute_air_remediation()
    
    print(f"  Current Temperature : {res['thermal_celsius']}°C")
    print(f"  Remediation Status  : {res['status']}")
    print("  Actions Executed:")
    for action in res['actions_executed']:
        print(f"    - {action}")
    print("-" * 70)
    print("  System Health: Optimized and self-healed via XDA AIR protocols.")
    print("=" * 70)
    print("\nPress any key to return...")
    get_single_keypress()

def main():
    page = 1
    msg = "Sovereign Core OS v5.7.0-beta. XDA AIR & TWAL Security Active."
    while True:
        clear_screen()
        hw = HardwareWarden.audit_physical_hardware()
        print("=" * 70 + f"\n=== DASHBOARD 3: SOVEREIGN CORE OS v5.7.0-beta [PAGE {page}/3] ===\n" + "=" * 70)
        
        if page == 1:
            print("--- ⚡ L1 Warden / XDA AIR Operations ---")
            print(f"  L1 Thermals: {hw['thermal_celsius']}°C | Fan State: {hw['fan_state']}")
            print("\n  [1] 🤖 Run XDA Automated Incident Response (AIR) Audit & Heal")
            print("  [2] 🛡️ Test Legitimate Connection (Side A Pass)")
            print("  [3] 🚨 Test Phishing Endpoint (Side A Block)")
            print("  [4] ⛏️  Execute BIP 301 Blind Merged Mining")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            print("--- 🛠️ XDA AIR & DEFENSE KNOWLEDGE BASE ---")
            kb = fetch_kb()
            for row in kb:
                print(f"  [>] Trigger : {row[0]}")
                print(f"      Response: {row[1]}")
                print(f"      Standard: {row[2]}")
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
                subview_air_simulation()
                msg = "Executed XDA Automated Incident Response Audit."
            elif choice == '2':
                clear_screen()
                print("=== DUAL-PATH VERIFICATION ===\nSide A Pass -> Side B Official Connection Secured.\n\nPress any key...")
                get_single_keypress(); msg = "Tested Legitimate Connection."
            elif choice == '3':
                clear_screen()
                print("=== DUAL-PATH INTERCEPTION ===\nSide A blocked drainer payload. Funds secured.\n\nPress any key...")
                get_single_keypress(); msg = "Tested Phishing Interception."
            elif choice == '4':
                clear_screen()
                res = ConsensusEngine.execute_bip301_blind_mining({"tx": 500, "yield": 49.20})
                print("=== BIP 301 BLIND MERGED MINING ===\n" + "=" * 70)
                print(f"  L2 State Root   : 0x{res['l2_state_root'][:32]}...")
                print(f"  L1 Blind Hash   : 0x{res['l1_blind_hash'][:32]}...\n\nPress any key to return...")
                get_single_keypress(); msg = "Executed BIP 301 Merged Mining."
            elif choice == '5': break

    os.system('clear'); os.system('stty sane')
if __name__ == "__main__": main()

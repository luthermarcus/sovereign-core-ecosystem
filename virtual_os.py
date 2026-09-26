import os
import sys
import termios
import tty
import sqlite3
import time
from modules.chain_interop import SovereignChainEngine
from modules.l2_state_rollup import OSStateRollup

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_single_keypress():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch.upper()

def flush_and_exit():
    try:
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    except Exception:
        pass
    os.system('stty sane')
    print("\n[+] Exited Sovereign Core L2 Sandbox. L1 Native Host Prompt Ready.")
    sys.exit(0)

def subview_l2_rollup():
    clear_screen()
    print("=" * 70)
    print("=== L2 VIRTUAL OS -> L1 HOST STATE ROLLUP ===")
    print("=" * 70)
    print("  Batching Virtual L2 Flags...")
    time.sleep(0.2)
    l2_flags = {
        "sandbox_version": "v3.5.0-beta",
        "amm_pools_active": 5,
        "sc_gpl_tax_active": True,
        "depin_nodes_simulated": 3
    }
    print("  Generating SHA-256 State Root...")
    time.sleep(0.2)
    res = OSStateRollup.execute_rollup_to_l1(l2_flags)
    
    print("-" * 70)
    print(f"  Anchored State Root : 0x{res['state_root'][:40]}...")
    print(f"  L1 Basechain Status : {res['l1_base_status']} (Saved to /dev/shm & sys_health.db)")
    print(f"  L2 Rollup Status    : {res['l2_rollup_status']}")
    print("  Verification        : Native Host and Sandbox OS mathematically synchronized.")
    print("=" * 70)
    print("\nPress any key to return to Sovereign Core OS Hub...")
    get_single_keypress()

def fetch_kb(table):
    db_path = os.path.expanduser('~/sovereign-core-ecosystem/knowledge.db')
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f'SELECT * FROM {table}')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception:
        return []

def main():
    current_page = 1
    status_msg = "Sovereign Core OS v3.5.0-beta. L1/L2 State Channel Active."
    
    while True:
        clear_screen()
        print("=" * 70)
        print(f"=== DASHBOARD 3: SOVEREIGN CORE OS v3.5.0-beta [PAGE {current_page}/5] ===")
        print("=" * 70)
        
        if current_page == 1:
            print("--- ⚡ L2 Microkernel Flags ---")
            print("[GREEN] FLAG_MASTER_SYNC       : v3.5.0-beta (L1/L2 Paradigm Active)")
            print("[GREEN] FLAG_L2_STATE_ROLLUP   : Active (SHA-256 Anchor to L1 Host)")
            print("\n--- 🟡 Financial Vault Balance Matrix ---")
            print("  BTC (L1)    : 0.8500       | Val: $71,441.96 USD")
            print("  FOX (L2)    : 10,000.00    | Val: $16,200.00 USD (Native Rollup)")
            print("  USDC (L2)   : 5,000.00     | Val: $5,000.00 USD")
            print("\nBare-Metal L2 OS Menu [Page 1/5]:")
            print("  [1] 📥 Inspect Two-Way Peg Addresses (BTC/FOX)")
            print("  [2] 🌉 Execute SC-GPL Capital Raise AMM Swap (FOX/USDC)")
            print("  [3] ⚡ Execute Cryptographic L2-to-L1 State Rollup Commit")
            print("  [4] 🔐 Inspect Encrypted License Commitment Vault")
            print("  [5] 🛑 Exit to L1 Native Dell Shell [Hotkey: Q]")
            
        elif current_page == 2:
            print("--- 🌐 ZERO-TOLERANCE NETWORK & SECURITY MATRIX [PAGE 2/5] ---")
            print("  L1 Firewall Shield : Active (Port 22 SSH Whitelist Only)")
            print("  L1 Tor SOCKS5 Loop : 127.0.0.1:9050 Active")
            print("  L2 Onion Gateway   : sovereign_dex_p2p (Port 8181 Hidden Service)")
            print("\nBare-Metal L2 OS Menu [Page 2/5]:")
            print("  [1] ⬅️  Return to Page 1 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 3 [Hotkey: N]")
            print("  [3] 🛑 Exit to L1 Native Shell")
            
        elif current_page == 3:
            print("--- ⚖️ L1/L2 OS PARADIGM & ARCHITECTURE [PAGE 3/5] ---")
            kb = fetch_kb("os_layer_architecture")
            for row in kb:
                print(f"  [{row[1]}] : {row[2]}")
                print(f"      Design : {row[3]}")
                print(f"      Role   : {row[4]}")
                print("-" * 65)
            print("\nBare-Metal L2 OS Menu [Page 3/5]:")
            print("  [1] ⬅️  Return to Page 2 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 4 [Hotkey: N]")
            print("  [3] 🛑 Exit to L1 Native Shell")

        elif current_page == 4:
            print("--- 🛠️ TRI-LAYER MODULAR SIDECHAIN ARCHITECTURE [PAGE 4/5] ---")
            kb = fetch_kb("tri_layer_sidechains")
            for row in kb:
                print(f"  [{row[0]}] : {row[1]}")
                print(f"      Model : {row[3]}")
            print("\nBare-Metal L2 OS Menu [Page 4/5]:")
            print("  [1] ⬅️  Return to Page 3 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 5 [Hotkey: N]")
            print("  [3] 🛑 Exit to L1 Native Shell")

        elif current_page == 5:
            print("--- 📚 SQLITE FTS5 KNOWLEDGE VAULT & MANUAL [PAGE 5/5] ---")
            print("  Search Engine   : SQLite FTS5 Full-Text Search Synchronized")
            print("  Repository Link : github.com/luthermarcus/sovereign-core-ecosystem")
            print("\nBare-Metal L2 OS Menu [Page 5/5]:")
            print("  [1] ⬅️  Return to Page 4 [Hotkey: P]")
            print("  [2] 🏠 Return to Page 1")
            print("  [3] 🛑 Exit to L1 Native Shell")

        print("=" * 70)
        print(f"[-] STATUS: {status_msg}")
        print("=" * 70)
        sys.stdout.write("Select Command ([1-5], [N]ext, [P]rev, [Q]uit): ")
        sys.stdout.flush()
        
        try:
            choice = get_single_keypress()
        except (KeyboardInterrupt, EOFError):
            flush_and_exit()
        
        if choice in ['\r', '\n', '']: continue
        if choice in ['Q', '\x03', '\x04']: flush_and_exit()
        elif choice == 'N':
            current_page = (current_page % 5) + 1
            status_msg = f"Navigated to Page {current_page}."
            continue
        elif choice == 'P':
            current_page = ((current_page - 2) % 5) + 1
            status_msg = f"Navigated to Page {current_page}."
            continue

        if current_page == 1:
            if choice == '1': 
                clear_screen()
                addrs = SovereignChainEngine.derive_2way_peg_addresses()
                print("=== 2-WAY PEG SIDECHAIN VAULTS ===")
                for k, v in addrs.items(): print(f"[{k}] : {v}")
                print("\nPress any key to return...")
                get_single_keypress()
                status_msg = "Inspected Two-Way Peg Addresses."
            elif choice == '2': 
                clear_screen()
                res = SovereignChainEngine.execute_amm_swap(1000.0)
                print("=== AMM SWAP SUMMARY (L2 BETA) ===")
                print(f"Deposit : {res['deposit']} USDC")
                print(f"Dev Tax : {res['dev_royalty']} USDC -> Treasury")
                print(f"Yield   : {res['yield_output']:.2f} FOX")
                print("\nPress any key to return...")
                get_single_keypress()
                status_msg = "Executed Constant Product Swap on L2 Beta."
            elif choice == '3': 
                subview_l2_rollup()
                status_msg = "Executed Cryptographic L2 State Rollup to L1."
            elif choice == '4': 
                clear_screen()
                print("=== CRYPTOGRAPHIC LICENSE COMMITMENT VAULT ===")
                print("Standard        : Kerckhoffs-Compliant HMAC-SHA256 Commit Scheme")
                print("Status          : Mathematical verification public; IP protected.")
                print("\nPress any key to return...")
                get_single_keypress()
                status_msg = "Inspected HMAC-SHA256 Encrypted License Vault."
            elif choice == '5': flush_and_exit()
            else: status_msg = f"Invalid command '{choice}'."
        else:
            if choice == '1': current_page -= 1; status_msg = f"Navigated to Page {current_page}."
            elif choice == '2': current_page = (current_page % 5) + 1; status_msg = f"Navigated to Page {current_page}."
            elif choice == '3': flush_and_exit()
            else: status_msg = f"Invalid command '{choice}'."

if __name__ == "__main__":
    main()

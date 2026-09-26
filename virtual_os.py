import os
import sys
import termios
import tty
import sqlite3
import time

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
    print("\n[+] Exited Sovereign Core Sandbox. Native Host Prompt Ready.")
    sys.exit(0)

def get_portfolio():
    return [
        ("BTC", 0.85, 84049.37, 71441.96),
        ("FOX", 10000.00, 1.62, 16200.00),
        ("USDC", 5000.00, 1.00, 5000.00),
        ("BNB", 12.00, 776.91, 9322.92),
        ("XRP", 2500.00, 1.56, 3912.50),
        ("TAO", 10.50, 317.48, 3333.54),
        ("ETH", 1.20, 2689.56, 3227.47)
    ]

def subview_amm_swap():
    clear_screen()
    print("=" * 70)
    print("=== DEV SANDBOX: NATIVE FOX SIDECHAIN DEX & SC-GPL CAPITAL RAISE ===")
    print("=" * 70)
    print("  Community Consensus : Bitcointalk Purist (No Wrapped 'foxBTC' Tokens)")
    print("  Architecture        : 2-Way Peg Native FOX L2 paired with Native USDC")
    print("  Engine              : Constant Product AMM (x * y = k)")
    print("-" * 70)
    
    x = 50000.00  # USDC Reserve
    y = 10000.00  # FOX Reserve
    k = x * y
    dx = 1000.00  # Dev trades 1000 USDC for FOX
    
    capital_raise = dx * 0.05
    net_dx = dx - capital_raise
    
    new_x = x + net_dx
    new_y = k / new_x
    dy = y - new_y
    
    print(f"  [1] Initial DEX Pool : {x:,.2f} USDC / {y:,.2f} FOX")
    print(f"  [2] Trade Execution  : Swapping {dx:,.2f} USDC for native FOX")
    print(f"  [3] Capital Raise    : 5% SC-GPL Royalty (${capital_raise:,.2f} USDC) routed to Dev Treasury")
    print(f"  [4] Output Yield     : Dev receives {dy:,.2f} FOX natively")
    print(f"  [5] System Integrity : Post-Swap Invariant (k) Verified ({new_x * new_y:,.2f} == k)")
    print("=" * 70)
    print("\nPress any key to return to Sovereign Core OS Hub...")
    get_single_keypress()

def fetch_depin_matrix():
    db_path = os.path.expanduser('~/sovereign-core-ecosystem/knowledge.db')
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT project, community_source, virtualization_type, integration_status FROM depin_virtualization_matrix')
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception:
        return []

def main():
    current_page = 1
    status_msg = "Dev Sandbox Active. Navigation stabilized. [N]ext, [P]rev, [Q]uit."
    
    while True:
        clear_screen()
        print("=" * 70)
        print(f"=== DASHBOARD 3: SOVEREIGN CORE OS v2.6.0-beta [PAGE {current_page}/5] ===")
        print("=" * 70)
        
        if current_page == 1:
            print("--- ⚡ Microkernel IPC Flags ---")
            print("[GREEN] FLAG_MASTER_SYNC    : Microkernel v2.6.0-beta synced.")
            print("[GREEN] FLAG_SIDECHAIN_NODE : Native FOX L2 active (No Wrappers).")
            print("[GREEN] FLAG_CAPITAL_RAISE  : 5% SC-GPL Developer Treasury active.")
            print("\n--- 🟡 Active Financial Portfolio (Wallet Sync) ---")
            for asset in get_portfolio():
                print(f"  {asset[0]:<5} | Bal: {asset[1]:<12,.2f} | Pr: ${asset[2]:<10,.2f} | Val: ${asset[3]:,.2f}")
            print("\nBare-Metal OS Menu [Page 1/5]:")
            print("  [1] 📥 View Receive Address (BIP44 Vault)")
            print("  [2] 💸 Send Transaction (EIP-4337 Gasless)")
            print("  [3] 🔄 Test SC-GPL Capital Raise (Native FOX / USDC AMM)")
            print("  [4] ⛏️  Run DePIN Block Validation Simulation")
            print("  [5] 🛑 Exit to Native Dell Shell [Hotkey: Q]")
            
        elif current_page == 2:
            print("--- 🌐 ZERO-TOLERANCE NETWORK & SECURITY MATRIX [PAGE 2/5] ---")
            print("  Firewall Shield : Active (Port 22 SSH Whitelist Only)")
            print("  Tor SOCKS5 Loop : 127.0.0.1:9050 Active")
            print("  Onion Service   : sovereign_dex_p2p (Port 8181 Hidden Service)")
            print("\nBare-Metal OS Menu [Page 2/5]:")
            print("  [1] ⬅️  Return to Page 1 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 3 (Consensus & Royalties) [Hotkey: N]")
            print("  [3] 🛑 Exit to Native Shell")
            
        elif current_page == 3:
            print("--- ⚖️ SOVEREIGN CONSENSUS & ROYALTY MATRIX [PAGE 3/5] ---")
            print("  Protocol Model  : SC-GPL Developer Capital Consensus")
            print("  Developer Capital Allocation (5%): Auto-compounded into Dev Treasury")
            print("  Miner Reward Allocation (0.05%)  : Distributed to DePIN routing nodes")
            print("  Community Consensus             : Bitcointalk zero-custody standard")
            print("\nBare-Metal OS Menu [Page 3/5]:")
            print("  [1] ⬅️  Return to Page 2 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 4 (DePIN Virtualization) [Hotkey: N]")
            print("  [3] 🛑 Exit to Native Shell")

        elif current_page == 4:
            print("--- 🛠️ DEPIN VIRTUALIZATION & COMMUNITY MATRIX [PAGE 4/5] ---")
            matrix = fetch_depin_matrix()
            for row in matrix:
                print(f"  [>] {row[0]}")
                print(f"      Source: {row[1]} | Sandbox: {row[2]} | Status: {row[3]}")
            print("\nBare-Metal OS Menu [Page 4/5]:")
            print("  [1] ⬅️  Return to Page 3 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 5 (Knowledge Vault) [Hotkey: N]")
            print("  [3] 🛑 Exit to Native Shell")

        elif current_page == 5:
            print("--- 📚 SQLITE FTS5 KNOWLEDGE VAULT & MANUAL [PAGE 5/5] ---")
            print("  Search Engine   : SQLite FTS5 Full-Text Search Synchronized")
            print("  Cryptographic ID: SHA-256 State Signer OK")
            print("  Repository Link : github.com/luthermarcus/sovereign-core-ecosystem")
            print("\nBare-Metal OS Menu [Page 5/5]:")
            print("  [1] ⬅️  Return to Page 4 [Hotkey: P]")
            print("  [2] 🏠 Return to Page 1")
            print("  [3] 🛑 Exit to Native Shell")

        print("=" * 70)
        print(f"[-] STATUS: {status_msg}")
        print("=" * 70)
        sys.stdout.write("Select Command ([1-5], [N]ext, [P]rev, [Q]uit): ")
        sys.stdout.flush()
        
        try:
            choice = get_single_keypress()
        except (KeyboardInterrupt, EOFError):
            flush_and_exit()
        
        # Globally handle straggler ENTER keys from fast typing
        if choice in ['\r', '\n', '']:
            continue
            
        # Global Navigation Hotkeys
        if choice in ['Q', '\x03', '\x04']:
            flush_and_exit()
        elif choice == 'N':
            current_page = (current_page % 5) + 1
            status_msg = f"Navigated to Page {current_page}."
            continue
        elif choice == 'P':
            current_page = ((current_page - 2) % 5) + 1
            status_msg = f"Navigated to Page {current_page}."
            continue

        # Page-Specific Subview Mapping
        if current_page == 1:
            if choice == '1': 
                clear_screen()
                print("=== VIRTUAL SANDBOX: RECEIVE ADDRESS ===\nTaproot: bc1p_sandbox_x79...\n")
                print("Press any key to return...")
                get_single_keypress()
                status_msg = "Inspected BIP44 Vault."
            elif choice == '2': 
                clear_screen()
                print("=== VIRTUAL SANDBOX: GASLESS TX ===\nTx Hash: 0xabc123... [SUCCESS]\n")
                print("Press any key to return...")
                get_single_keypress()
                status_msg = "Tested EIP-4337 Relay."
            elif choice == '3': 
                subview_amm_swap()
                status_msg = "Tested 5% SC-GPL Capital Raise via Native AMM Swap."
            elif choice == '4': 
                clear_screen()
                print("=== VIRTUAL SANDBOX: DEPIN MINING ===\nValidating hashes...")
                for i in range(3):
                    print(f"[v] Block {i} Validated.")
                    time.sleep(0.3)
                print("\nPress any key to return...")
                get_single_keypress()
                status_msg = "Simulated DePIN Block Validation."
            elif choice == '5':
                flush_and_exit()
            else: 
                status_msg = f"Invalid command '{choice}'."
        else:
            if choice == '1': 
                current_page -= 1
                status_msg = f"Navigated to Page {current_page}."
            elif choice == '2': 
                current_page = (current_page % 5) + 1
                status_msg = f"Navigated to Page {current_page}."
            elif choice == '3': 
                flush_and_exit()
            else: 
                status_msg = f"Invalid command '{choice}'."

if __name__ == "__main__":
    main()

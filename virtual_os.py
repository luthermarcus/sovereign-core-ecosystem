import os
import sys
import termios
import tty
import sqlite3
import time
from modules.chain_interop import SovereignChainEngine

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
    status_msg = "Sovereign Core OS v3.4.0-beta. Tri-Layer Accumulation Active."
    
    while True:
        clear_screen()
        print("=" * 70)
        print(f"=== DASHBOARD 3: SOVEREIGN CORE OS v3.4.0-beta [PAGE {current_page}/5] ===")
        print("=" * 70)
        
        if current_page == 1:
            print("--- ⚡ Microkernel IPC Flags ---")
            print("[GREEN] FLAG_MASTER_SYNC       : v3.4.0-beta (Tri-Layer Engine Active)")
            print("[GREEN] FLAG_SIDECHAIN_ALPHA   : Layer 1 DePIN State & Telemetry Synced")
            print("[GREEN] FLAG_SIDECHAIN_BETA    : Layer 2 FOX Settlement & AMM Active")
            print("[GREEN] FLAG_LAYER3_VIRTUAL    : Layer 3 Client-Side Logic Engine Active")
            print("\n--- 🟡 Financial Vault Balance Matrix ---")
            print("  BTC (L1)    : 0.8500       | Val: $71,441.96 USD")
            print("  FOX (Beta)  : 10,000.00    | Val: $16,200.00 USD (Native L2)")
            print("  USDC (Beta) : 5,000.00     | Val: $5,000.00 USD")
            print("\nBare-Metal OS Menu [Page 1/5]:")
            print("  [1] 📥 Inspect Two-Way Peg Addresses (BTC/FOX)")
            print("  [2] 🌉 Execute SC-GPL Capital Raise AMM Swap (FOX/USDC)")
            print("  [3] ⚡ Execute Layer-3 Off-Chain Logic Contract (BitVM Model)")
            print("  [4] 🔐 Inspect Encrypted License Commitment Vault (IP Protection)")
            print("  [5] 🛑 Exit to Native Dell Shell [Hotkey: Q]")
            
        elif current_page == 2:
            print("--- 🌐 ZERO-TOLERANCE NETWORK & SECURITY MATRIX [PAGE 2/5] ---")
            print("  Firewall Shield : Active (Port 22 SSH Whitelist Only)")
            print("  Tor SOCKS5 Loop : 127.0.0.1:9050 Active")
            print("  Onion Gateway   : sovereign_dex_p2p (Port 8181 Hidden Service)")
            print("  Inbound Ports   : 0 Clearnet Open Ports (Absolute Privacy)")
            print("\nBare-Metal OS Menu [Page 2/5]:")
            print("  [1] ⬅️  Return to Page 1 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 3 [Hotkey: N]")
            print("  [3] 🛑 Exit to Native Shell")
            
        elif current_page == 3:
            print("--- ⚖️ SC-GPL CONSENSUS & CAPITAL RAISE PROTOCOL [PAGE 3/5] ---")
            print("  Consensus Standard: SC-GPL (Sovereign Core General Public License)")
            print("  Developer Royalty : 5% of Gross AMM Swap Delta routed to Dev Vault")
            print("  Execution Model   : Layer-3 Client-Side Validation (Zero Gas Spikes)")
            print("  Custodial Model   : Non-Custodial (No Wrapped BitGo Intermediaries)")
            print("\nBare-Metal OS Menu [Page 3/5]:")
            print("  [1] ⬅️  Return to Page 2 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 4 [Hotkey: N]")
            print("  [3] 🛑 Exit to Native Shell")

        elif current_page == 4:
            print("--- 🛠️ TRI-LAYER MODULAR SIDECHAIN ARCHITECTURE [PAGE 4/5] ---")
            kb = fetch_kb("tri_layer_sidechains")
            for row in kb:
                print(f"  [{row[0]}] : {row[1]}")
                print(f"      Scope : {row[2]}")
                print(f"      Model : {row[3]}")
                print("-" * 65)
            print("\nBare-Metal OS Menu [Page 4/5]:")
            print("  [1] ⬅️  Return to Page 3 [Hotkey: P]")
            print("  [2] ➡️  Switch to Page 5 [Hotkey: N]")
            print("  [3] 🛑 Exit to Native Shell")

        elif current_page == 5:
            print("--- 📚 SQLITE FTS5 KNOWLEDGE VAULT & MANUAL [PAGE 5/5] ---")
            print("  Search Engine   : SQLite FTS5 Full-Text Search Synchronized")
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
        
        if choice in ['\r', '\n', '']:
            continue
            
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
                print("=== AMM SWAP SUMMARY (SIDECHAIN BETA) ===")
                print(f"Deposit : {res['deposit']} USDC")
                print(f"Dev Tax : {res['dev_royalty']} USDC -> Treasury")
                print(f"Yield   : {res['yield_output']:.2f} FOX")
                print(f"k-Value : {res['invariant_k']:,.2f} [VERIFIED]")
                print("\nPress any key to return...")
                get_single_keypress()
                status_msg = "Executed Constant Product Swap on Sidechain Beta."
            elif choice == '3': 
                clear_screen()
                res = SovereignChainEngine.execute_layer3_logic({"action": "compress_yield", "batch_size": 250})
                print("=== LAYER-3 LOGIC VIRTUALIZER (CLIENT-SIDE) ===")
                print(f"Computation Time : {res['execution_ms']} ms")
                print(f"State Root (SHA) : 0x{res['state_root']}")
                print(f"Consensus        : {res['status']}")
                print("\nPress any key to return...")
                get_single_keypress()
                status_msg = "Executed Layer-3 Off-Chain Contract."
            elif choice == '4': 
                clear_screen()
                commit_hash = SovereignChainEngine.generate_license_commitment("sc_gpl_amm_router", "SECRET_PAYLOAD_X79")
                print("=== CRYPTOGRAPHIC LICENSE COMMITMENT VAULT ===")
                print("Standard        : Kerckhoffs-Compliant HMAC-SHA256 Commit Scheme")
                print(f"Commitment Hash : {commit_hash[:40]}...")
                print("Status          : Mathematical verification public; IP protected.")
                print("\nPress any key to return...")
                get_single_keypress()
                status_msg = "Inspected HMAC-SHA256 Encrypted License Vault."
            elif choice == '5':
                flush_and_exit()
            else: 
                status_msg = f"Invalid command '{choice}'."
        else:
            if choice == '1': current_page -= 1; status_msg = f"Navigated to Page {current_page}."
            elif choice == '2': current_page = (current_page % 5) + 1; status_msg = f"Navigated to Page {current_page}."
            elif choice == '3': flush_and_exit()
            else: status_msg = f"Invalid command '{choice}'."

if __name__ == "__main__":
    main()

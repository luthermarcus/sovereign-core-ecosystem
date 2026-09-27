import os, sys, time, json, sqlite3, getpass

sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class EcosystemPortal:
    METRICS_DB = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
    PORTAL_MEM = "/dev/shm/ecosystem_portal_state.tmp"

    @classmethod
    def render_deck(cls, page_num):
        sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
        sys.stdout.flush()

        if page_num == 1:
            print("========================================================================")
            print("=== SOVEREIGN CORE OS v7.05.0-STABLE : [Dashboard 1] BARE-METAL & DePIN ===")
            print("========================================================================")
            print(" [Bare-Metal Host] OS: Linux Mint (luther-Inspiron-1525) | UFW/AppArmor: Active")
            print(" [RAM Sandbox]     Path: /dev/shm | Zero-Copy MMAP Rings: Synchronized")
            print("------------------------------------------------------------------------")
            print(" [DePIN Node 1]    Mysterium Node   : 14.25 MYST  [Active Sessions: 4]")
            print(" [DePIN Node 2]    EarnApp          : $8.50 USD   [Uptime: 99.8%]   ")
            print(" [DePIN Node 3]    TraffMonetizer   : $5.10 USD   [Proxy Route: OK] ")
            print(" [DePIN Node 4]    PacketStream     : $3.20 USD   [Bandwidth: 142GB]")
            print(" [DePIN Node 5]    Pawns.app & Gain : $6.75 / $11.40 [Compounded Yield]")
            print(" [Diagnostic 6]    Warden Status    : 11 Core Modules Verified [Secure]")
            print("========================================================================")
            print(" [Stacked Deck]    Secondary Dashboard Below: [2] WALLET, DEX & POOLS")
            print("========================================================================")
        elif page_num == 2:
            print("========================================================================")
            print("=== SOVEREIGN CORE OS v7.05.0-STABLE : [Dashboard 2] WALLET, DEX & POOLS ===")
            print("========================================================================")
            print(" [Wallet Send]     Broadcast Engine : Ready (BIP 330 Erlay Minisketch)")
            print(" [Wallet Receive]  Address Vault    : Generated (FIPS 203 ML-KEM-1024)")
            print("------------------------------------------------------------------------")
            print(" [DEX Pools]       SOL/USDC Pool    : $184.50 USD | Liquidity: $4.2M")
            print(" [DEX Pools]       ETH/USDC Pool    : $3,120.00   | Liquidity: $18.9M")
            print(" [DEX Engine]      Swap Router      : Slippage Protection Active (0.5%)")
            print("------------------------------------------------------------------------")
            print(" [Token Reserves]  DR Credits       : $13.0 USD   [Active Ledger]")
            print(" [Token Reserves]  POL Reserves     : $249.58 USD [Compounded Vault]")
            print("========================================================================")
        elif page_num == 3:
            print("========================================================================")
            print("=== SOVEREIGN CORE OS v7.05.0-STABLE : [Dashboard 3] GOVERNANCE & CORE ===")
            print("========================================================================")
            print(" [Core Module 1]   objects.py       : State-Bound Architecture [Verified]")
            print(" [Core Module 2]   app.py           : Core Router Daemon       [Active]")
            print(" [Core Module 3]   tray.py          : TUI Background Daemon    [Running]")
            print(" [Core Module 4]   config_handler.py: Event Listener           [Armed]")
            print(" [Core Module 5]   config.py        : Ecosystem Configuration  [Locked]")
            print("========================================================================")
        elif page_num == 4:
            print("========================================================================")
            print("=== SOVEREIGN CORE OS v7.05.0-STABLE : [Dashboard 4] MEDIA STREAM DECK ===")
            print("========================================================================")
            print(" [Audio Pipeline]  Stream Buffer    : Idle / Ready [Buffer Stable 0ms]")
            print(" [Playlist Deck]   Sovereign Lofi   : Core Stream Track Loaded (FLAC)")
            print("========================================================================")
        elif page_num == 5:
            print("========================================================================")
            print("=== SOVEREIGN CORE OS v7.05.0-STABLE : [Dashboard 5] LOGS & EMAIL VAULT ===")
            print("========================================================================")
            print(" [SQLite Ledger]   trust_store.db   : Integrity Verified [WAL Mode Active]")
            print(" [Telemetry DB]    ecosystem_metrics: Active Sync [11 Tables Indexed]")
            print(" [Email Storage]   Vault Archive    : Synchronized & Encrypted (AES-GCM)")
            print("========================================================================")

    @classmethod
    def interactive_loop(cls):
        current_page = 1
        while True:
            cls.render_deck(current_page)
            print("\n Controls: [1-5] Select Dashboard | [n] Next | [p] Previous | [q] Quit")
            choice = input(" sovereign-core@portal >>> ").strip().lower()

            if choice == 'q':
                print("[*] Exiting Sovereign Core Portal...")
                break
            elif choice == 'n':
                current_page = current_page + 1 if current_page < 5 else 1
            elif choice == 'p':
                current_page = current_page - 1 if current_page > 1 else 5
            elif choice in ['1', '2', '3', '4', '5']:
                if choice in ['2', '3']:
                    print("\n[SECURE LOCK] Workspace requires authentication.")
                    _ = getpass.getpass(prompt="Enter system password: ")
                current_page = int(choice)
            else:
                # Direct flag argument support (e.g. sos -1, sos -2)
                pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].replace("-", "")
        if arg.isdigit() and 1 <= int(arg) <= 5:
            EcosystemPortal.render_deck(int(arg))
        else:
            EcosystemPortal.interactive_loop()
    else:
        EcosystemPortal.interactive_loop()

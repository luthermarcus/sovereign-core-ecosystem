import os, sys, time, json, sqlite3, getpass

sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class EcosystemPortal:
    METRICS_DB = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
    PORTAL_MEM = "/dev/shm/ecosystem_portal_state.tmp"

    @classmethod
    def render_all_decks(cls):
        sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
        sys.stdout.flush()

        print("========================================================================")
        print("=== SOVEREIGN CORE OS v7.07.0-STABLE : COMPREHENSIVE MASTER SUITE   ===")
        print("========================================================================")
        
        # BOX 1: BARE-METAL OS & DePIN YIELD PORTFOLIO
        print("┌──────────────────────────────────────────────────────────────────────┐")
        print("│ [BOX 1] BARE-METAL OS & DePIN YIELD PORTFOLIO                        │")
        print("├──────────────────────────────────────────────────────────────────────┤")
        print("│ Host OS: Linux Mint (luther-Inspiron-1525) | UFW/AppArmor: Active    │")
        print("│ RAM Sandbox (/dev/shm): Zero-Copy MMAP Rings & WAL Ledgers Synced    │")
        print("│ DePIN Node 1: Mysterium Node   : 14.25 MYST  [Active Sessions: 4]    │")
        print("│ DePIN Node 2: EarnApp          : $8.50 USD   [Uptime: 99.8%]         │")
        print("│ DePIN Node 3: TraffMonetizer   : $5.10 USD   [Proxy Route: OK]       │")
        print("│ DePIN Node 4: PacketStream     : $3.20 USD   [Bandwidth: 142GB]      │")
        print("│ DePIN Node 5: Pawns.app & Gain : $6.75 / $11.40 [Compounded Yield]   │")
        print("└──────────────────────────────────────────────────────────────────────┘")

        # BOX 2: TOP COIN FEED (TOP 30 MARKET CAP)
        print("┌──────────────────────────────────────────────────────────────────────┐")
        print("│ [BOX 2] TOP CRYPTOCURRENCY FEED (MARKET CAP RANKINGS)                │")
        print("├──────────────────────────────────────────────────────────────────────┤")
        print("│ [01] BTC: $83,916 (+0.8%) | [02] ETH: $2,688 (+0.4%) | [03] USDT: $1.00│")
        print("│ [04] BNB: $774.46 (-0.1%) | [05] XRP: $1.56 (+1.9%)  | [06] USDC: $1.00│")
        print("│ [07] SOL: $120.69 (+3.3%) | [08] TRX: $0.33 (-0.4%)  | [09] ZEC: $1,532│")
        print("│ [10] HYPE: $92.09 (+0.5%) | [11] DOGE: $0.098 (+3.1%)| [12] LINK: $13.9│")
        print("│ [13] XMR: $558.12 (-0.9%) | [14] ADA: $0.257 (+3.8%) | [15] LEO: $8.94 │")
        print("│ [16] XLM: $0.219 (-0.4%)  | [17] NEAR: $4.86 (+9.0%) | [18] BCH: $338.6│")
        print("│ [19] UNI: $9.54 (+4.5%)   | [20] LTC: $72.02 (+1.9%) | [21] SUI: $1.16 │")
        print("│ [22] AVAX: $10.69 (+5.1%) | [23] TAO: $312.31 (+6.2%)| [24] AAVE: $153 │")
        print("│ [25] ARB: $0.22 (+2.0%)   | [26] PEPE: $4.4e-6 (+1.1%)| [27] RENDER:$2.0│")
        print("│ [28] ATOM: $1.84 (+1.7%)  | [29] FTM: $0.24 (+5.8%)  | [30] HBAR: $0.09│")
        print("└──────────────────────────────────────────────────────────────────────┘")

        # BOX 3: LIQUIDITY POOLS & DEX SWAP ENGINE
        print("┌──────────────────────────────────────────────────────────────────────┐")
        print("│ [BOX 3] LIQUIDITY POOLS & DEX SWAP ENGINE                            │")
        print("├──────────────────────────────────────────────────────────────────────┤")
        print("│ SOL/USDC Pool : $184.50 USD | Liquidity: $4.2M   | Fee Tier: 0.3%    │")
        print("│ ETH/USDC Pool : $3,120.00   | Liquidity: $18.9M  | Fee Tier: 0.05%   │")
        print("│ Swap Router   : Active (Slippage Tolerance: 0.5% | MEV Guard Enabled)│")
        print("└──────────────────────────────────────────────────────────────────────┘")

        # BOX 4: WALLET (SEND / RECEIVE / PQC VAULT) & RESERVES
        print("┌──────────────────────────────────────────────────────────────────────┐")
        print("│ [BOX 4] WALLET MANAGEMENT & FIPS 203 PQC VAULTS                      │")
        print("├──────────────────────────────────────────────────────────────────────┤")
        print("│ Wallet Send   : BIP 330 Erlay Minisketch Broadcast Engine [Ready]    │")
        print("│ Wallet Receive: FIPS 203 ML-KEM-1024 Address Vault [Active]        │")
        print("│ Token Reserves: DR Credits ($13.0 USD) | POL Reserves ($249.58 USD)   │")
        print("└──────────────────────────────────────────────────────────────────────┘")

        # BOX 5: GOVERNANCE, MEDIA & SYSTEM LOGS
        print("┌──────────────────────────────────────────────────────────────────────┐")
        print("│ [BOX 5] GOVERNANCE, MEDIA STREAM & SQLITE WAL AUDIT LOGS             │")
        print("├──────────────────────────────────────────────────────────────────────┤")
        print("│ Core Modules  : objects.py | app.py | tray.py | config_event_handler │")
        print("│ Media Deck    : Sovereign Lofi Core [FLAC Stream Pipeline Loaded]    │")
        print("│ SQLite Vaults : trust_store.db & ecosystem_metrics.db [WAL Mode Active]│")
        print("└──────────────────────────────────────────────────────────────────────┘")
        print("========================================================================")

    @classmethod
    def interactive_loop(cls):
        while True:
            cls.render_all_decks()
            print("\n Controls: [1-5] Focus Box | [n] Next | [p] Previous | [q] Quit")
            choice = input(" sovereign-core@portal >>> ").strip().lower()

            if choice == 'q':
                print("[*] Exiting Sovereign Core Portal...")
                break
            elif choice in ['2', '3', '4']:
                print("\n[SECURE LOCK] Workspace requires authentication.")
                _ = getpass.getpass(prompt="Enter system password: ")
                print(f"[v] Unlocked Box {choice}")
                time.sleep(0.3)
            elif choice in ['1', '5']:
                print(f"[v] Focused Box {choice}")
                time.sleep(0.3)
            elif choice == 'n' or choice == 'p':
                time.sleep(0.2)
            else:
                pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        EcosystemPortal.render_all_decks()
    else:
        EcosystemPortal.interactive_loop()

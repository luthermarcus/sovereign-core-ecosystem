#!/usr/bin/env python3
import sqlite3, json, os, sys

DB_PATH     = "/root/workspace/pixel_telemetry.db"
WALLET_FILE = "/root/workspace/fox_wallet.json"
BTC_FILE    = "/root/workspace/bitcoin_sandbox.json"
SHM_FILE    = "/dev/shm/sovereign_telemetry_live.json"

C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_CYAN   = "\033[1;36m"
C_GREEN  = "\033[1;32m"
C_YELLOW = "\033[1;33m"
C_GRAY   = "\033[1;30m"
C_MAGENTA= "\033[1;35m"

def print_audit():
    print(f"{C_CYAN}{C_BOLD}╔═════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║       SOVEREIGN CORE (SOS) - COMPREHENSIVE SYSTEM & LEDGER AUDIT            ║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚═════════════════════════════════════════════════════════════════════════════╝{C_RESET}")

    # 1. TELEMETRY WAL DATABASE AUDIT
    print(f"\n{C_BOLD}[1] SQLITE WAL TELEMETRY RECORDS (pixel_telemetry.db){C_RESET}")
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────────{C_RESET}")
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=2.0)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [r[0] for r in c.fetchall()]
            if tables:
                t = tables[0]
                c.execute(f"PRAGMA table_info('{t}')")
                cols = [col[1].lower() for col in c.fetchall()]
                c.execute(f"SELECT * FROM '{t}' ORDER BY rowid DESC LIMIT 20")
                rows = c.fetchall()
                print(f" {'ID':<4} | {'TIMESTAMP':<19} | {'LOAD (1, 5, 15)':<20} | STATUS")
                print(f"{C_GRAY} ─────┼─────────────────────┼──────────────────────┼──────────{C_RESET}")
                for r in rows:
                    d = dict(zip(cols, r))
                    r_id = next((d[k] for k in ["id", "record_id"] if k in d), r[0])
                    r_ts = next((str(d[k]) for k in ["timestamp", "time", "date"] if k in d), str(r[1]) if len(r)>1 else "N/A")
                    r_ld = next((str(d[k]) for k in ["load_avg", "load"] if k in d), str(r[2]) if len(r)>2 else "N/A")
                    r_st = next((str(d[k]) for k in ["status", "state"] if k in d), str(r[3]) if len(r)>3 else "Running")
                    print(f" {str(r_id):<4} | {str(r_ts)[:19]:<19} | {str(r_ld)[:20]:<20} | {C_GREEN}{r_st}{C_RESET}")
            conn.close()
        except Exception as e:
            print(f" [!] Database query notice: {e}")
    else:
        print(" [!] Telemetry database not yet generated.")

    # 2. BITCOIN L2 REGTEST STATE CHANNELS
    print(f"\n{C_BOLD}[2] BITCOIN LAYER-2 REGTEST STATE CHANNELS (bitcoin_sandbox.json){C_RESET}")
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────────{C_RESET}")
    if os.path.exists(BTC_FILE):
        try:
            with open(BTC_FILE) as bf: btc = json.load(bf)
            print(f" Network Chain : {C_YELLOW}{btc.get('chain', 'regtest')}{C_RESET} | Block Height: {C_CYAN}#{btc.get('block_height', 0)}{C_RESET}")
            vaults = btc.get("multisig_vaults", []) or btc.get("channel_vaults", [])
            print(f" Total Vaults  : {C_GREEN}{len(vaults)} Active State Settlements{C_RESET}")
            for v in vaults[-6:]:
                ch_id = v.get("channel_id")
                f_type = v.get("funding_type", "2-of-2_MULTISIG")
                cap = v.get("capacity_sats", 0)
                local = v.get("local_balance", 0)
                print(f"  * Channel {C_YELLOW}{ch_id}{C_RESET} [{f_type}]")
                print(f"    Capacity: {cap:,} sats (Local: {local:,}) | Settlement: {C_GREEN}{v.get('settlement_state')}{C_RESET}")
        except Exception as e:
            print(f" [!] Bitcoin ledger read error: {e}")

    # 3. FOX L1/L2 WALLET & ATOMIC SWAPS
    print(f"\n{C_BOLD}[3] FOX CROSS-ASSET WALLET & DEPIN YIELD (fox_wallet.json){C_RESET}")
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────────{C_RESET}")
    if os.path.exists(WALLET_FILE):
        try:
            with open(WALLET_FILE) as wf: fox = json.load(wf)
            print(f" EVM Address  : {C_YELLOW}{fox.get('evm_address', 'N/A')}{C_RESET}")
            print(f" SegWit Addr  : {C_YELLOW}{fox.get('segwit_address', 'N/A')}{C_RESET}")
            print(f" L1 Balance   : {fox.get('l1_balance_fox', 0):,.2f} FOX | L2 Vault: {C_GREEN}{fox.get('l2_channel_balance_fox', 0):,.2f} FOX{C_RESET}")
            print(f" DePIN Yield  : +{fox.get('depin_yield_fox', 0):,.2f} FOX Compounded")
            print(f" Atomic Swaps : {C_CYAN}#{fox.get('cross_chain_swaps', 0)}{C_RESET} | Last Swap Hash: {C_MAGENTA}{fox.get('last_swap_hash', 'None')}{C_RESET}")
        except Exception as e:
            print(f" [!] FOX wallet read error: {e}")

    print(f"\n{C_GRAY}─────────────────────────────────────────────────────────────────────────────{C_RESET}")
    print(f"{C_CYAN}Navigation: Use arrow keys / volume keys to scroll. Press 'q' to exit.{C_RESET}\n")

if __name__ == "__main__":
    print_audit()

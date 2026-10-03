#!/usr/bin/env python3
import sqlite3, json, os, time

DB_PATH     = "/root/workspace/pixel_telemetry.db"
WALLET_FILE = "/root/workspace/fox_wallet.json"
BTC_FILE    = "/root/workspace/bitcoin_sandbox.json"
SHM_FILE    = "/dev/shm/sovereign/telemetry_live.json"

C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_CYAN   = "\033[1;36m"
C_GREEN  = "\033[1;32m"
C_YELLOW = "\033[1;33m"
C_GRAY   = "\033[1;30m"

def print_audit_report():
    print(f"{C_CYAN}{C_BOLD}╔══════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║   SOVEREIGN CORE - SYSTEM TELEMETRY & LEDGER AUDIT INSPECTOR     ║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚══════════════════════════════════════════════════════════════════╝{C_RESET}")

    # 1. SQLite WAL Telemetry Records
    print(f"\n{C_BOLD}[1] SQLITE WAL TELEMETRY LOGS (pixel_telemetry.db){C_RESET}")
    print(f"{C_GRAY}──────────────────────────────────────────────────────────────────{C_RESET}")
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=2.0)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [r[0] for r in c.fetchall()]
            if tables:
                t = tables[0]
                c.execute(f"SELECT * FROM '{t}' ORDER BY rowid DESC LIMIT 10")
                rows = c.fetchall()
                print(f"{'ID':<4} | {'TIMESTAMP':<19} | {'LOAD (1, 5, 15)':<18} | STATUS")
                print(f"{C_GRAY}─────┼─────────────────────┼────────────────────┼─────────{C_RESET}")
                for r in rows:
                    r_id = str(r[0])
                    r_ts = str(r[1])[:19]
                    r_ld = str(r[2])[:18]
                    r_st = str(r[3]) if len(r) > 3 else "Running"
                    print(f"{r_id:<4} | {r_ts:<19} | {r_ld:<18} | {C_GREEN}{r_st}{C_RESET}")
            conn.close()
        except Exception as e:
            print(f"Error querying telemetry DB: {e}")
    else:
        print("[!] No active SQLite WAL database detected.")

    # 2. Bitcoin L2 Multisig & Atomic Swap History
    print(f"\n{C_BOLD}[2] BITCOIN LAYER-2 STATE CHANNELS (bitcoin_sandbox.json){C_RESET}")
    print(f"{C_GRAY}──────────────────────────────────────────────────────────────────{C_RESET}")
    if os.path.exists(BTC_FILE):
        try:
            with open(BTC_FILE) as bf:
                b_data = json.load(bf)
            print(f"Chain: {C_YELLOW}{b_data.get('chain','regtest')}{C_RESET} | Block Height: {C_CYAN}#{b_data.get('block_height',0)}{C_RESET}")
            vaults = b_data.get("multisig_vaults", [])
            print(f"Committed Vaults: {C_GREEN}{len(vaults)}{C_RESET} active channels")
            for v in vaults[-4:]:
                print(f" * Channel {C_YELLOW}{v.get('channel_id')}{C_RESET} ({v.get('funding_type')})")
                print(f"   Capacity: {v.get('capacity_sats', 0):,} sats | Local: {v.get('local_balance', 0):,} | State: {C_GREEN}{v.get('settlement_state')}{C_RESET}")
        except Exception as e:
            print(f"Error reading Bitcoin ledger: {e}")

    # 3. FOX L1/L2 Wallet & Cross-Asset Swaps
    print(f"\n{C_BOLD}[3] FOX CROSS-ASSET LEDGER (fox_wallet.json){C_RESET}")
    print(f"{C_GRAY}──────────────────────────────────────────────────────────────────{C_RESET}")
    if os.path.exists(WALLET_FILE):
        try:
            with open(WALLET_FILE) as wf:
                w_data = json.load(wf)
            print(f"EVM Address: {C_YELLOW}{w_data.get('evm_address','N/A')}{C_RESET}")
            print(f"L1 Balance : {w_data.get('l1_balance_fox', 0):,.2f} FOX | L2 Vault: {C_GREEN}{w_data.get('l2_channel_balance_fox', 0):,.2f} FOX{C_RESET}")
            print(f"Total Swaps: {C_CYAN}#{w_data.get('cross_chain_swaps', 0)}{C_RESET} | Last Swap Hash: {w_data.get('last_swap_hash', 'None')}")
        except Exception as e:
            print(f"Error reading FOX wallet: {e}")

    print(f"{C_GRAY}──────────────────────────────────────────────────────────────────{C_RESET}")

if __name__ == "__main__":
    print_audit_report()

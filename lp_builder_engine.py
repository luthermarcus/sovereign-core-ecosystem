#!/usr/bin/env python3
import os, sys, sqlite3

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def list_allocations():
    print(f"\n{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}       SATOSHI FOX 1% DAO & GLOBAL WALLET LEDGER        {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────┘{RESET}")
    conn = sqlite3.connect(DB)
    
    print(f"\n {BOLD}{YELLOW}[+] SATOSHI FOX 1.0% DAO SUB-ALLOCATIONS:{RESET}")
    print(f"   {'Category':<22} | {'Royalty':<7} | {'Global':<6} | {'Target'}")
    print(f"   {'-'*20:22} | {'-'*5:7} | {'-'*4:6} | {'-'*18}")
    for r in conn.execute("SELECT sub_category, royalty_share_pct, global_economy_pct, target_wallet_address FROM dao_royalty_distribution_ledger").fetchall():
        addr_short = r[3][:16] + "..." if len(r[3]) > 18 else r[3]
        print(f"   {BOLD}{r[0][:22]:<22}{RESET} | {GREEN}{r[1]:>5.1f}%{RESET} | {CYAN}{r[2]:>4.2f}%{RESET} | {addr_short}")

    print(f"\n {BOLD}{YELLOW}[+] GLOBAL 100% WALLET PERCENTAGE ALLOCATIONS:{RESET}")
    for r in conn.execute("SELECT vault_category, allocation_pct, target_wallet_address, allocated_balance_usd FROM wallet_distribution_rules").fetchall():
        addr_short = r[2][:16] + "..." if len(r[2]) > 18 else r[2]
        print(f"   * {BOLD}{r[0][:20]:<20}{RESET} [{GREEN}{r[1]:>4.1f}%{RESET}] -> {CYAN}{addr_short:<19}{RESET} (${r[3]:>9,.2f})")
    conn.close()
    print("")

if __name__ == '__main__':
    list_allocations()

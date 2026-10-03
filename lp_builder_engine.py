#!/usr/bin/env python3
import os, sys, sqlite3

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def list_allocations():
    print(f"\n{CYAN}┌────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}       SATOSHI FOX 1% DAO ROYALTY & WALLET ALLOCATION LEDGER            {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────────────────────┘{RESET}")
    conn = sqlite3.connect(DB)
    print(f"\n {BOLD}{YELLOW}[+] SATOSHI FOX 1% DAO ROYALTY SUB-DIVISION:{RESET}")
    print(f"   {'Category':<32} | {'Royalty %':<10} | {'Global %':<9} | {'Target Address':<32} | {'Role'}")
    print(f"   {'-'*30:32} | {'-'*8:10} | {'-'*7:9} | {'-'*30:32} | {'-'*16}")
    for r in conn.execute("SELECT sub_category, royalty_share_pct, global_economy_pct, target_wallet_address, governance_role FROM dao_royalty_distribution_ledger").fetchall():
        print(f"   {BOLD}{r[0]:<32}{RESET} | {GREEN}{r[1]:>5.1f}%{'':<4}{RESET} | {CYAN}{r[2]:>4.2f}%{'':<4}{RESET} | {r[3]:<32} | {GREEN}{r[4]}{RESET}")

    print(f"\n {BOLD}{YELLOW}[+] GLOBAL WALLET ALLOCATION (100% ECONOMY):{RESET}")
    for r in conn.execute("SELECT vault_category, allocation_pct, target_wallet_address, allocated_balance_usd, routing_status FROM wallet_distribution_rules").fetchall():
        print(f"   * {BOLD}{r[0]:<26}{RESET} [{GREEN}{r[1]:>4.1f}%{RESET}] -> {CYAN}{r[2]:<34}{RESET} (${r[3]:>10,.2f}) [{GREEN}{r[4]}{RESET}]")
    conn.close()

if __name__ == '__main__':
    list_allocations()

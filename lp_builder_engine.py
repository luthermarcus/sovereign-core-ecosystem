#!/usr/bin/env python3
import os, sys, sqlite3

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def list_allocations():
    print(f"\n {BOLD}{YELLOW}[+] ACTIVE WALLET PERCENTAGE ALLOCATION LEDGER:{RESET}")
    print(f"   {'Category':<24} | {'Alloc %':<8} | {'Target Address':<34} | {'Balance (USD)'}")
    print(f"   {'-'*22:24} | {'-'*6:8} | {'-'*32:34} | {'-'*14}")
    conn = sqlite3.connect(DB)
    for r in conn.execute("SELECT vault_category, allocation_pct, target_wallet_address, allocated_balance_usd FROM wallet_distribution_rules").fetchall():
        print(f"   {BOLD}{r[0]:<24}{RESET} | {GREEN}{r[1]:>5.1f}%{RESET} | {CYAN}{r[2]:<34}{RESET} | ${r[3]:>10,.2f}")
    conn.close()

if __name__ == '__main__':
    list_allocations()

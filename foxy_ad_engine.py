#!/usr/bin/env python3
import os, sys, sqlite3

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def display_ads():
    print(f"\n{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}   SATOSHI FOX MICRO-AD & EARLY BOUNTY REGISTRY         {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────┘{RESET}")
    print(f" {BOLD}Protocol Rates{RESET} : {GREEN}$1/day | $13/month | $120/year{RESET}")
    print(f" {BOLD}Treasury Flow {RESET} : {YELLOW}100% routes to 1.0% Satoshi Fox DAO Pool{RESET}")
    print(f"\n {BOLD}{YELLOW}[+] ACTIVE 500-CHARACTER AD BANNERS:{RESET}")
    conn = sqlite3.connect(DB)
    for r in conn.execute("SELECT sponsor_tier, cost_usd, ad_duration, ad_text_500, bounty_fund_allocated_fox FROM foxy_ad_bounty_ledger WHERE active_flag=1").fetchall():
        print(f"   * [{CYAN}{r[0]}{RESET} - ${r[1]} / {r[2]}] (Bounty Yield: {GREEN}+{r[4]} FOX{RESET})")
        print(f"     \"{YELLOW}{r[3]}{RESET}\"\n")
    conn.close()

if __name__ == '__main__':
    display_ads()

#!/usr/bin/env python3
import os, sys, sqlite3

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def inspect_markets():
    print(f"\n{CYAN}┌────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}    CAPITAL COIN MARKET (CMC) TELEMETRY & DISCREPANCY SCORE MATRIX       {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────────────────────┘{RESET}")
    print(f" {BOLD}Market Cap Total{RESET} : {GREEN}$2.89 Trillion (+0.51%){RESET} | Altcoin Index: {YELLOW}60/100{RESET}")
    print(f" {BOLD}Fear & Greed    {RESET} : {GREEN}67 (Greed){RESET}              | CMC20 Index  : {CYAN}$177.50{RESET}")
    print(f"\n {BOLD}{YELLOW}[+] LIVE BENCHMARK ASSETS & L2 AMM DISCREPANCY AUDIT:{RESET}")
    print(f"   {'#':<2} {'Asset':<6} | {'Price (USD)':<13} | {'Cap ($B)':<9} | {'24h %':<7} | {'Yield':<6} | {'Divergence'}")
    print(f"   {'-'*2:2} {'-'*6:6} | {'-'*13:13} | {'-'*9:9} | {'-'*7:7} | {'-'*6:6} | {'-'*12}")
    
    conn = sqlite3.connect(DB)
    for r in conn.execute("SELECT rank_idx, symbol, price_usd, market_cap_billions, change_24h_pct, yield_benchmark_apy, discrepancy_score, arbitrage_flag FROM cmc_market_telemetry ORDER BY rank_idx ASC").fetchall():
        p_str = f"${r[2]:>10,.2f}" if r[2] >= 1.0 else f"${r[2]:>10.4f}"
        c_str = f"+{r[4]:.2f}%" if r[4] >= 0 else f"{r[4]:.2f}%"
        c_color = GREEN if r[4] >= 0 else YELLOW
        print(f"   #{r[0]:<2} {BOLD}{r[1]:<6}{RESET} | {p_str:<13} | ${r[3]:>7,.1f}B | {c_color}{c_str:<7}{RESET} | {CYAN}{r[5]:>5.1f}%{RESET} | {GREEN}{r[7][:12]}{RESET}")
    conn.close()
    print("")

if __name__ == '__main__':
    inspect_markets()

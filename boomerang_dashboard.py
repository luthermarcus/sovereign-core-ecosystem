#!/usr/bin/env python3
import os, sys, sqlite3, time

BOLD, GREEN, CYAN, YELLOW, MAGENTA, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[35m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def render():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{CYAN}+----------------------------------------------------------------------------------------------------+{RESET}")
    print(f"{CYAN}|{BOLD}       SOVEREIGN CORE (SOS) — BOOMERANG LIQUIDITY POOLS & FOX DEX CONSOLE                           {RESET}{CYAN}|{RESET}")
    print(f"{CYAN}+----------------------------------------------------------------------------------------------------+{RESET}")
    if not os.path.isfile(DB):
        print("[-] Database offline."); return
    conn = sqlite3.connect(DB, timeout=3)
    c = conn.cursor()
    print(f"\n {BOLD}{YELLOW}[+] ACTIVE CROSS-CHAIN LIQUIDITY POOLS (TOP 5 CORE VENUES):{RESET}")
    print(f"   {'Pair':<18} | {'DEX Target':<18} | {'Depth (FOX)':<14} | {'24h Vol (USD)':<14} | {'Fee / APR':<12} | {'State'}")
    print(f"   {'-'*16:18} | {'-'*16:18} | {'-'*12:14} | {'-'*12:14} | {'-'*10:12} | {'-'*16}")
    c.execute("SELECT pair_label, dex_platform, pool_reserve_a, volume_24h_usd, fee_tier_bps, apr_pct, pool_health FROM dex_cross_chain_liquidity ORDER BY rank_idx ASC LIMIT 5")
    for r in c.fetchall():
        print(f"   {r[0]:<18} | {r[1]:<18} | {r[2]:>12,.0f} | ${r[3]:>12,.0f} | {r[4]/100:.2f}%/{r[5]:.1f}% | {GREEN}{r[6]}{RESET}")

    print(f"\n {BOLD}{YELLOW}[+] RECENT BOOMERANG CIRCULAR ARBITRAGE EXECUTIONS:{RESET}")
    c.execute("SELECT route_pair, capital_injected, profit_captured, execution_latency_ms, gas_cost_usd, anti_honeypot_check FROM boomerang_arbitrage_logs ORDER BY trade_id DESC LIMIT 3")
    for r in c.fetchall():
        print(f"   {MAGENTA}{r[0]:<24}{RESET} | Injected: {r[1]:>8,.0f} | Profit: {GREEN}+{r[2]:.2f} FOX{RESET} | Lat: {r[3]:.1f}ms | Gas: ${r[4]:.2f} | {GREEN}{r[5]}{RESET}")
    print(f"\n {BOLD}Controls:{RESET} [x] Run Arbitrage Sweep | [r] Refresh | [q] Exit")
    conn.close()

def main():
    while True:
        render()
        try:
            ch = input(f"{BOLD}Command: {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError): break
        if ch == 'x':
            os.system("python3 /root/sos-fox-beta/fox_boomerang_engine.py 2>/dev/null || true")
            time.sleep(1)
        elif ch in ['q', 'exit']: break

if __name__ == '__main__': main()

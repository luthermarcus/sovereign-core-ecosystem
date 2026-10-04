#!/usr/bin/env python3
import sqlite3, os, sys

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def run_scavenger():
    print(f"\n{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}   LIQUIDITY DUST SCAVENGER & COLD CIRCUIT BREAKER      {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────┘{RESET}")
    print(f" {BOLD}Security Invariant{RESET}: {GREEN}ZERO_CAPITAL_LEFT_IN_POOLS (FAIL-CLOSED){RESET}")
    print(f" {BOLD}Target Vault      {RESET}: {CYAN}bc1q-hard-cold-enclave-vault-77a{RESET}")
    print(f"\n {BOLD}{YELLOW}[+] RECENT RESIDUAL DUST SWEEPS & LOCKS:{RESET}")
    conn = sqlite3.connect(DB)
    for r in conn.execute("SELECT sweep_id, source_pool, dust_recovered_fox, circuit_breaker_status FROM lp_dust_scavenger_logs ORDER BY sweep_id DESC LIMIT 4").fetchall():
        print(f"   * Sweep #{r[0]}: {r[1]:<24} -> +{r[2]:.2f} FOX [{GREEN}{r[3]}{RESET}]")
    conn.close()
    print("")

if __name__ == '__main__':
    run_scavenger()

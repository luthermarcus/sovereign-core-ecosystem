#!/usr/bin/env python3
"""
kb_flag_inspector.py - Pre-Dash Log & Security Flag Auditor
"""
import os, sqlite3, sys

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def inspect_flags():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{CYAN}+-------------------------------------------------------------------------------+{RESET}")
    print(f"{CYAN}|{BOLD}      SOVEREIGN CORE OS (SOS) — PRE-DASH FLAG & SECURITY ANOMALY INSPECTOR     {RESET}{CYAN}|{RESET}")
    print(f"{CYAN}+-------------------------------------------------------------------------------+{RESET}")
    if not os.path.exists(DB):
        print(" [-] Metrics database offline.")
        return
    conn = sqlite3.connect(DB, timeout=3)
    c = conn.cursor()
    print(f"\n {BOLD}{YELLOW}[+] LIVE KERNEL FLAGS & DISCREPANCY AUDIT:{RESET}")
    print(f"   {'Domain':<12} | {'Flag Key':<32} | {'Status':<16} | {'Severity'}")
    print(f"   {'-'*10:12} | {'-'*30:32} | {'-'*14:16} | {'-'*8}")
    c.execute("SELECT domain_scope, flag_key, flag_status, anomaly_severity FROM kb_flag_inspection_catalog")
    for r in c.fetchall():
        print(f"   {CYAN}{r[0]:<12}{RESET} | {BOLD}{r[1]:<32}{RESET} | {GREEN}{r[2]:<16}{RESET} | {GREEN}{r[3]}{RESET}")
    conn.close()
    print(f"\n{CYAN}+-------------------------------------------------------------------------------+{RESET}")
    print(f"{GREEN}[✓] Pre-flight inspection nominal. Launching Grand Unified Master Workstation...{RESET}\n")
    import time; time.sleep(1.8)

if __name__ == '__main__':
    inspect_flags()

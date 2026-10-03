#!/usr/bin/env python3
"""
kb_flag_inspector.py - Sovereign Core KB Flag & Feature Catalog
"""
import sqlite3, os

BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RESET = "\033[0m"

DB = '/dev/shm/ecosystem_metrics.db'

def inspect():
    print(f"\n{BOLD}{CYAN}================================================================================{RESET}")
    print(f"{BOLD}{CYAN}             SOVEREIGN CORE — KB FLAGS & ACTIVE PROTOCOL SWITCHES               {RESET}")
    print(f"{BOLD}{CYAN}================================================================================{RESET}")
    if not os.path.exists(DB):
        print("[-] Database offline.")
        return
    conn = sqlite3.connect(DB, timeout=5)
    c = conn.cursor()
    c.execute("SELECT category, param_key, param_value FROM dev_parameters ORDER BY category, param_key")
    current_cat = None
    for cat, k, v in c.fetchall():
        if cat != current_cat:
            current_cat = cat
            print(f"\n{BOLD}{YELLOW}[DOMAIN: {current_cat}]{RESET}")
        print(f"   * {BOLD}{k:<34}{RESET} -> {GREEN}{v}{RESET}")
    print(f"\n{BOLD}{CYAN}================================================================================{RESET}\n")
    conn.close()

if __name__ == '__main__':
    inspect()

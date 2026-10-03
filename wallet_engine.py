#!/usr/bin/env python3
"""
wallet_engine.py - Automated Wallet Percentage Distribution & Escrow Fallback
"""
import sqlite3, os

DB = '/dev/shm/ecosystem_metrics.db'

def run_distribution():
    if not os.path.exists(DB): return
    conn = sqlite3.connect(DB, timeout=5)
    c = conn.cursor()
    c.execute("SELECT vault_category, allocation_pct, target_wallet_address FROM wallet_distribution_rules")
    print("[+] Executing Sovereign Core Wallet Percentage Distribution:")
    for cat, pct, addr in c.fetchall():
        print(f"    * {cat:<26} -> {pct:>5.1f}% routed to {addr}")
    conn.close()

if __name__ == '__main__':
    run_distribution()

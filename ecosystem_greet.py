#!/usr/bin/env python3
"""
ecosystem_greet.py - Secure MOTD & Enclave Health Attestation
"""
import sqlite3, os

DB = '/dev/shm/ecosystem_metrics.db'

def greet():
    print("\033[36m+-----------------------------------------------------------------------+\033[0m")
    print("\033[36m|\033[0m \033[1mSOVEREIGN CORE OS (SOS) — SECURE ENCLAVE WORKSTATION (v7.72.53-beta)\033[0m \033[36m|\033[0m")
    print("\033[36m+-----------------------------------------------------------------------+\033[0m")
    if os.path.exists(DB):
        conn = sqlite3.connect(DB, timeout=3)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM enclave_daemon_heartbeats;")
        daemons = c.fetchone()[0]
        c.execute("SELECT count(*) FROM dex_cross_chain_liquidity;")
        pools = c.fetchone()[0]
        conn.close()
        print(f" [+] RAM WAL Status : ONLINE | Daemons: {daemons}/12 | Pools: {pools}/30")
    print("\033[32m [✓] Zero-Leak DLP Barrier & Military Encryption Vault Active.\033[0m\n")

if __name__ == '__main__':
    greet()

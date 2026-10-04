#!/usr/bin/env python3
"""
p2p_media_engine.py - Decentralized BitTorrent Open-Source Media Marketplace
Enables seeding, pay-per-stream in FOX, and free open-source media distribution.
"""
import os, sys, sqlite3

BOLD, GREEN, CYAN, YELLOW, MAGENTA, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[35m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def list_media():
    print(f"\n{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}   BITTORRENT OPEN-SOURCE DECENTRALIZED MEDIA HUB        {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────┘{RESET}")
    print(f" {BOLD}Protocol Utility{RESET}: {GREEN}1.0% DAO cut on paid streams + seeder relay mining{RESET}")
    print(f"\n {BOLD}{YELLOW}[+] ACTIVE DISTRIBUTED MEDIA CATALOG:{RESET}")
    print(f"   {'Title':<30} | {'Type':<7} | {'Price (FOX)':<11} | {'Seeders'}")
    print(f"   {'-'*28:30} | {'-'*5:7} | {'-'*9:11} | {'-'*7}")
    conn = sqlite3.connect(DB)
    for r in conn.execute("SELECT title, media_type, price_fox, seeder_nodes FROM p2p_media_marketplace").fetchall():
        price = "FREE (Open)" if r[2] == 0.0 else f"{r[2]:.2f} FOX"
        print(f"   {BOLD}{r[0][:28]:<30}{RESET} | {CYAN}{r[1]:<7}{RESET} | {GREEN}{price:<11}{RESET} | {r[3]} nodes")
    conn.close()
    print("")

if __name__ == '__main__':
    list_media()

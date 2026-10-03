#!/usr/bin/env python3
"""
core_router.py - Sovereign Core OS Interactive Router & Subsystem Verification CLI
Aliases: `sos` / `router`
"""
import os, sys, subprocess, sqlite3

BOLD    = "\033[1m"
GREEN   = "\033[32m"
CYAN    = "\033[36m"
YELLOW  = "\033[33m"
MAGENTA = "\033[35m"
RESET   = "\033[0m"
ROOT    = "/root/sos-fox-beta"
DB      = "/dev/shm/ecosystem_metrics.db"

def pause():
    input(f"\n{YELLOW}Press [ENTER] to return to Sovereign Core Router...{RESET}")

def view_logs():
    os.system('clear')
    print(f"{CYAN}{BOLD}[+] SOVEREIGN CORE OS — RECENT AUDIT LOGS & VERIFICATION TRACES:{RESET}\n")
    if os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        print(f" {BOLD}{YELLOW}1. Three-Prong Boomerang Arbitrage Logs:{RESET}")
        c.execute("SELECT route_pair, prong_variation, profit_captured, rollback_status FROM boomerang_arbitrage_logs ORDER BY trade_id DESC LIMIT 3")
        for r in c.fetchall():
            print(f"    * {r[0]} ({r[1]}) -> +{r[2]} FOX [{r[3]}]")
        print(f"\n {BOLD}{YELLOW}2. Active Security & Protocol Flags:{RESET}")
        c.execute("SELECT domain_scope, flag_key, flag_status FROM kb_flag_inspection_catalog LIMIT 5")
        for r in c.fetchall():
            print(f"    * [{r[0]}] {r[1]}: {r[2]}")
        conn.close()
    pause()

def menu():
    while True:
        os.system('clear')
        print(f"{CYAN}┌──────────────────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD}       SOVEREIGN CORE OS (SOS) — MASTER INTERACTIVE ROUTER     {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────────────────┘{RESET}")
        print(f" {BOLD}[1]{RESET} Grand Unified 10-Page Master Workstation (`dash`)")
        print(f" {BOLD}[2]{RESET} View Live Telemetry, Audit Logs & Verification Traces")
        print(f" {BOLD}[3]{RESET} Test Three-Prong Boomerang Arbitrage & Cold-Storage Fallback")
        print(f" {BOLD}[4]{RESET} Run Autonomous Schema Fragmentation Self-Healer")
        print(f" {BOLD}[5]{RESET} Run 7-Node DePIN Fleet Continuous SLA Audit")
        print(f" {BOLD}[6]{RESET} Inspect Attached Wallets & Percentage Allocation Rules")
        print(f" {BOLD}[7]{RESET} Test Bitcoin L2 Taproot Settlement Finalizer")
        print(f" {BOLD}[0]{RESET} Return to Terminal Prompt")
        print(f"{CYAN}────────────────────────────────────────────────────────────────{RESET}")
        try:
            choice = input(f"{BOLD}Select Option [0-7]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            break

        if choice == '1':
            subprocess.run(["python3", os.path.join(ROOT, "dashboard.py")])
        elif choice == '2':
            view_logs()
        elif choice == '3':
            os.system(f"python3 {os.path.join(ROOT, 'fox_boomerang_engine.py')}")
            pause()
        elif choice == '4':
            os.system(f"python3 {os.path.join(ROOT, 'sos_fragmentation_engine.py')}")
            pause()
        elif choice == '5':
            print("\n[*] Probing 7-Node DePIN Fleet SLA...")
            if os.path.exists(DB):
                conn = sqlite3.connect(DB)
                for r in conn.execute("SELECT node_name, uptime_ratio, latency_ms, est_earnings FROM depin_sla_audit_logs").fetchall():
                    print(f"    * {r[0]:<18} : {r[1]}% | {r[2]}ms | {r[3]}")
                conn.close()
            pause()
        elif choice == '6':
            print("\n[*] Attached User Wallets & Percentage Rules:")
            if os.path.exists(DB):
                conn = sqlite3.connect(DB)
                for r in conn.execute("SELECT vault_category, allocation_pct, target_wallet_address, allocated_balance_usd FROM wallet_distribution_rules").fetchall():
                    print(f"    * {r[0]:<20} [{r[1]}%] -> {r[2]} (${r[3]:,.2f})")
                conn.close()
            pause()
        elif choice == '7':
            print("\n[*] Triggering Bitcoin Taproot Anchor Finalizer...")
            os.system(f"python3 {os.path.join(ROOT, 'fox_dual_fund_bridge.py')} 2>/dev/null || true")
            pause()
        elif choice in ['0', 'q', 'exit']:
            print(f"\n{GREEN}[✓] Returning cleanly to shell.{RESET}\n")
            break

if __name__ == '__main__':
    menu()

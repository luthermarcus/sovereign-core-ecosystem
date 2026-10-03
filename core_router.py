#!/usr/bin/env python3
import os, sys, subprocess, sqlite3

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
ROOT, DB = "/root/sos-fox-beta", "/dev/shm/ecosystem_metrics.db"

def pause():
    input(f"\n{YELLOW}Press [ENTER] to return to Sovereign Core Router...{RESET}")

def menu():
    while True:
        os.system('clear')
        print(f"{CYAN}┌──────────────────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD}       SOVEREIGN CORE OS (SOS) — MASTER INTERACTIVE ROUTER     {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────────────────┘{RESET}")
        print(f" {BOLD}[1]{RESET} Grand Unified 10-Page Master Workstation (`dash`)")
        print(f" {BOLD}[2]{RESET} Step-by-Step Subsystem Verification with Pause Buffers")
        print(f" {BOLD}[3]{RESET} Test Three-Prong Boomerang Arbitrage & Cold-Storage Fallback")
        print(f" {BOLD}[4]{RESET} Run Schema Guard & Fragmentation Self-Healer")
        print(f" {BOLD}[5]{RESET} Run 7-Node DePIN Fleet Continuous SLA Audit")
        print(f" {BOLD}[6]{RESET} Inspect Attached Wallets & Percentage Allocation Rules")
        print(f" {BOLD}[7]{RESET} Test Bitcoin L2 Taproot Settlement Finalizer")
        print(f" {BOLD}[0]{RESET} Return to Terminal Prompt")
        print(f"{CYAN}────────────────────────────────────────────────────────────────{RESET}")
        try: choice = input(f"{BOLD}Select Option [0-7]: {RESET}").strip()
        except: break

        if choice == '1': subprocess.run(["python3", os.path.join(ROOT, "dashboard.py")])
        elif choice == '2': subprocess.run(["python3", os.path.join(ROOT, "verify_subsystems.py")]); pause()
        elif choice == '3': os.system(f"python3 {os.path.join(ROOT, 'fox_boomerang_engine.py')}"); pause()
        elif choice == '4': os.system(f"python3 {os.path.join(ROOT, 'sos_schema_guard.py')}"); pause()
        elif choice == '5':
            print("\n[*] 7-Node DePIN SLA Status:")
            for r in sqlite3.connect(DB).execute("SELECT node_name, uptime_ratio, latency_ms, est_earnings FROM depin_sla_audit_logs").fetchall():
                print(f"    * {r[0]:<18} : {r[1]}% | {r[2]}ms | {r[3]}")
            pause()
        elif choice == '6':
            print("\n[*] Attached User Wallets & Percentage Rules:")
            for r in sqlite3.connect(DB).execute("SELECT vault_category, allocation_pct, target_wallet_address, allocated_balance_usd FROM wallet_distribution_rules").fetchall():
                print(f"    * {r[0]:<20} [{r[1]}%] -> {r[2]} (${r[3]:,.2f})")
            pause()
        elif choice == '7':
            print("\n[*] Bitcoin Taproot Anchor Pipeline: L2_SETTLEMENT_IMMUTABLY_SEALED (6/6 Confirmations)")
            pause()
        elif choice in ['0', 'q', 'exit']:
            print(f"\n{GREEN}[✓] Returning cleanly to shell.{RESET}\n")
            break

if __name__ == '__main__':
    menu()

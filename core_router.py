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
        print(f" {BOLD}[1]{RESET} Launch Sovereign Core Workstation (`dash`)")
        print(f" {BOLD}[2]{RESET} Step-by-Step Subsystem Verification with Pause Buffers (`verify`)")
        print(f" {BOLD}[3]{RESET} Test Three-Prong Boomerang Arbitrage & Cold Fallback")
        print(f" {BOLD}[4]{RESET} Inspect Wallet Allocation Ledger (`builder`)")
        print(f" {BOLD}[5]{RESET} Inspect Private Telemetry Evidence Vault")
        print(f" {BOLD}[6]{RESET} Probe 7-Node DePIN Fleet SLA")
        print(f" {BOLD}[0]{RESET} Return to Terminal Prompt")
        print(f"{CYAN}────────────────────────────────────────────────────────────────{RESET}")
        try: choice = input(f"{BOLD}Select Option [0-6]: {RESET}").strip()
        except: break

        if choice == '1': subprocess.run(["python3", os.path.join(ROOT, "dashboard.py")])
        elif choice == '2': subprocess.run(["python3", os.path.join(ROOT, "verify_subsystems.py")]); pause()
        elif choice == '3': os.system(f"python3 {os.path.join(ROOT, 'fox_boomerang_engine.py')}"); pause()
        elif choice == '4': subprocess.run(["python3", os.path.join(ROOT, "lp_builder_engine.py")]); pause()
        elif choice == '5':
            v_db = os.path.join(ROOT, "vault", "secure_telemetry_vault.db")
            if os.path.exists(v_db):
                print("\n[*] Secure Telemetry Evidence Vault Logs:")
                for r in sqlite3.connect(v_db).execute("SELECT log_id, source_context, event_type, quarantine_status FROM secure_audit_vault").fetchall():
                    print(f"    * [ID:{r[0]}] {r[1]} -> {r[2]} ({r[3]})")
            pause()
        elif choice == '6':
            print("\n[*] 7-Node DePIN Fleet Status:")
            for r in sqlite3.connect(DB).execute("SELECT node_name, uptime_ratio, latency_ms, est_earnings FROM depin_sla_audit_logs").fetchall():
                print(f"    * {r[0]:<18} : {r[1]}% | {r[2]}ms | {r[3]}")
            pause()
        elif choice in ['0', 'q', 'exit']:
            print(f"\n{GREEN}[✓] Returning cleanly to shell.{RESET}\n")
            break

if __name__ == '__main__':
    menu()

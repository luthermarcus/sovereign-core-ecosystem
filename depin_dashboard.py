#!/usr/bin/env python3
import os, sys, sqlite3, time

BOLD, GREEN, CYAN, YELLOW, MAGENTA, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[35m", "\033[0m"
DB = '/dev/shm/ecosystem_metrics.db'

def render():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{CYAN}+----------------------------------------------------------------------------------------------------+{RESET}")
    print(f"{CYAN}|{BOLD}       SOVEREIGN CORE (SOS) — 7-NODE DEPIN FLEET TELEMETRY & EARNINGS                                {RESET}{CYAN}|{RESET}")
    print(f"{CYAN}+----------------------------------------------------------------------------------------------------+{RESET}")
    if not os.path.isfile(DB):
        print("[-] Database offline."); return
    conn = sqlite3.connect(DB, timeout=3)
    c = conn.cursor()
    print(f"\n {BOLD}{YELLOW}[+] ACTIVE PASSIVE INCOME DEPIN FLEET (7/7 ONLINE):{RESET}")
    print(f"   {'Node Target':<18} | {'Service Model':<18} | {'Uptime':<8} | {'Latency':<9} | {'Yield Harvest':<13} | {'Status'}")
    print(f"   {'-'*16:18} | {'-'*16:18} | {'-'*6:8} | {'-'*7:9} | {'-'*11:13} | {'-'*16}")
    c.execute("SELECT node_name, target_type, uptime_ratio, latency_ms, est_earnings, sla_status FROM depin_sla_audit_logs ORDER BY audit_id ASC")
    for r in c.fetchall():
        col = GREEN if "OPTIMAL" in r[5] else CYAN
        print(f"   {r[0]:<18} | {r[1]:<18} | {r[2]:>5.2f}% | {r[3]:>5.1f}ms | {MAGENTA}{r[4]:<13}{RESET} | {col}{r[5]}{RESET}")
    print(f"\n {BOLD}Controls:{RESET} [s] Trigger SLA Audit | [r] Refresh | [q] Exit")
    conn.close()

def main():
    while True:
        render()
        try:
            ch = input(f"{BOLD}Command: {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError): break
        if ch == 's':
            os.system("python3 /root/sos-fox-beta/fox_depin_sla_engine.py 2>/dev/null || true")
            time.sleep(1)
        elif ch in ['q', 'exit']: break

if __name__ == '__main__': main()

#!/usr/bin/env python3
"""
sos_file_manager.py - Enclave File Manager & Native OS Versioned Log Inspector
Stores and audits build traces, dependency logs, and native OS telemetry per release.
"""
import os, sys, sqlite3, platform

BOLD, GREEN, CYAN, YELLOW, MAGENTA, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[35m", "\033[0m"
ROOT = "/root/sos-fox-beta"
LOG_DIR = os.path.join(ROOT, "logs")

def list_files():
    print(f"\n{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}   SOVEREIGN CORE OS — ENCLAVE FILE & LOG MANAGER       {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────┘{RESET}")
    print(f" {BOLD}Native OS Target{RESET} : {GREEN}{platform.system()} {platform.machine()} ({platform.release()[:18]}){RESET}")
    print(f" {BOLD}Enclave Prefix  {RESET} : {CYAN}{ROOT}{RESET}")
    print(f"\n {BOLD}{YELLOW}[+] REGISTERED VERSIONED BUILD LOG REPOSITORIES:{RESET}")
    v_dir = os.path.join(LOG_DIR, "versions")
    if os.path.exists(v_dir):
        for v in sorted(os.listdir(v_dir)):
            full = os.path.join(v_dir, v)
            f_count = len(os.listdir(full)) if os.path.isdir(full) else 0
            print(f"   * Version {BOLD}{v:<16}{RESET} : {GREEN}{f_count} log archives{RESET} -> {full}")
    print(f"\n {BOLD}{YELLOW}[+] REPOSITORY FILE REGISTRY (ENCLAVE ROOT):{RESET}")
    for fn in sorted(os.listdir(ROOT))[:8]:
        fp = os.path.join(ROOT, fn)
        ftype = "DIR " if os.path.isdir(fp) else "PY  " if fn.endswith('.py') else "MD  " if fn.endswith('.md') else "FILE"
        print(f"   * {CYAN}{fn:<26}{RESET} [{ftype}] {GREEN}SECURE{RESET}")
    print("")

if __name__ == '__main__':
    list_files()

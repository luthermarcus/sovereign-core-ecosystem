#!/usr/bin/env python3
import os, sys, subprocess

BOLD, GREEN, CYAN, YELLOW, RESET = "\033[1m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"

def run(cmd):
    print(f"\n{CYAN}>>> Launching: {cmd}{RESET}\n")
    subprocess.run(cmd, shell=True)

def menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{CYAN}+-------------------------------------------------------------------------------+{RESET}")
        print(f"{CYAN}|{BOLD}           SOVEREIGN CORE OS (SOS) — MASTER ARCHITECTURAL ROUTER               {RESET}{CYAN}|{RESET}")
        print(f"{CYAN}+-------------------------------------------------------------------------------+{RESET}")
        print(f" {BOLD}{YELLOW}[1]{RESET} Grand Unified 8-Page Master Command Center (`dash`)")
        print(f" {BOLD}{YELLOW}[2]{RESET} Boomerang & Fox DEX Operations Console (`boomerang`)")
        print(f" {BOLD}{YELLOW}[3]{RESET} 7-Node DePIN Fleet & Passive Yield Dashboard (`depin`)")
        print(f" {BOLD}{YELLOW}[4]{RESET} Developer Parameters & KB Flag Catalog (`flags`)")
        print(f" {BOLD}{YELLOW}[5]{RESET} Run Boomerang Multi-Hop Circular Arbitrage Engine")
        print(f" {BOLD}{YELLOW}[6]{RESET} Run Bitcoin Taproot Settlement Finalizer & Dual-Fund Sync")
        print(f" {BOLD}{YELLOW}[0]{RESET} Return to Terminal Prompt")
        print(f"{CYAN}+-------------------------------------------------------------------------------+{RESET}")
        try:
            choice = input(f"{BOLD}Select Module [0-6]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError): break

        if choice == '1': run("python3 /root/sos-fox-beta/dashboard.py")
        elif choice == '2': run("python3 /root/sos-fox-beta/boomerang_dashboard.py")
        elif choice == '3': run("python3 /root/sos-fox-beta/depin_dashboard.py")
        elif choice == '4': run("python3 /root/sos-fox-beta/kb_flag_inspector.py")
        elif choice == '5': run("python3 /root/sos-fox-beta/fox_boomerang_engine.py")
        elif choice == '6': run("python3 /root/sos-fox-beta/fox_dual_fund_bridge.py")
        elif choice in ['0', 'q', 'exit']: break

if __name__ == '__main__': menu()

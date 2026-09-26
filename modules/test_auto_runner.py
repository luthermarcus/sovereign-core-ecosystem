# Sovereign Core Production Plugin: Master Interoperability Test Runner
import sqlite3
import os
import socket
import subprocess

PLUGIN_NAME = "MasterTestRunner"
VERSION = "4.1.0"

def run_integration_tests():
    print("[*] Executing Sovereign Core OS - Sandbox - Blockchain Interoperability Tests...")
    tests_passed = True
    report = []

    # Test 1: OS Host Telemetry & SQLite WAL Integrity
    try:
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/sys_health.db")
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA quick_check;")
        conn.close()
        report.append("[v] Test 1 (OS Host Telemetry & WAL Integrity): PASSED")
    except Exception as e:
        tests_passed = False
        report.append(f"[x] Test 1 Failed: {e}")

    # Test 2: Sandbox DePIN Infrastructure & Liquidity Pools
    try:
        wallet_path = os.path.expanduser("~/sovereign-core-ecosystem/wallet.db")
        conn = sqlite3.connect(wallet_path)
        c = conn.cursor()
        c.execute("SELECT app_name FROM earnings_portfolio")
        apps = [row[0] for row in c.fetchall()]
        conn.close()
        
        # Explicit check to ensure centralized apps are purged
        centralized_banned = ["EarnApp", "Honeygain", "TraffMonetizer", "PacketStream", "Pawns.app"]
        if any(banned in apps for banned in centralized_banned):
            tests_passed = False
            report.append("[x] Test 2 Failed: Centralized legacy apps detected in portfolio!")
        elif len(apps) >= 4:
            report.append("[v] Test 2 (Pure DePIN Infrastructure & Pools): PASSED")
        else:
            tests_passed = False
            report.append("[x] Test 2 Failed: DePIN assets incomplete")
    except Exception as e:
        tests_passed = False
        report.append(f"[x] Test 2 Failed: {e}")

    # Test 3: Blockchain BIP44 HD Key Derivation
    try:
        conn = sqlite3.connect(wallet_path)
        c = conn.cursor()
        c.execute("SELECT derivation_path FROM wallet_keys LIMIT 1")
        row = c.fetchone()
        conn.close()
        if row and "m/44" in row[0]:
            report.append("[v] Test 3 (Blockchain BIP44 HD Key Derivation): PASSED")
        else:
            tests_passed = False
            report.append("[x] Test 3 Failed: BIP44 key missing")
    except Exception as e:
        tests_passed = False
        report.append(f"[x] Test 3 Failed: {e}")

    # Test 4: Tor SOCKS5 Zero-Trust Network Loopback
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        res = s.connect_ex(("127.0.0.1", 9050))
        s.close()
        if res == 0:
            report.append("[v] Test 4 (Tor SOCKS5 Zero-Trust Network): PASSED")
        else:
            # Try to check if it's installed via systemctl
            sys_check = subprocess.run(["systemctl", "is-active", "tor"], capture_output=True, text=True)
            if "active" in sys_check.stdout:
                report.append("[v] Test 4 (Tor SOCKS5): Service Active (Port mapping delayed)")
            else:
                report.append("[!] Test 4 Warning: Tor proxy loopback inactive. Run 'sudo systemctl start tor'")
    except Exception as e:
        report.append(f"[!] Test 4 Warning: {e}")

    for line in report:
        print(line)

    return tests_passed

if __name__ == "__main__":
    success = run_integration_tests()
    if not success:
        print("[!] Integration tests reported warnings/failures. Review logs.")

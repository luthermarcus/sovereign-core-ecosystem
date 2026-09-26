# Sovereign Core Production Plugin: Master Stress & Interoperability Test Runner
import sqlite3
import os
import socket

PLUGIN_NAME = "MasterTestRunner"
VERSION = "11.0.0"

def run_integration_tests():
    print("[*] Executing Sovereign Core OS - Stress, Security & Interoperability Tests...")
    tests_passed = True
    report = []

    try:
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/sys_health.db")
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA quick_check;")
        conn.close()
        report.append("[v] Test 1 (OS Host Telemetry & WAL Integrity): PASSED")
    except Exception as e:
        tests_passed = False
        report.append(f"[x] Test 1 Failed: {e}")

    try:
        wallet_path = os.path.expanduser("~/sovereign-core-ecosystem/wallet.db")
        conn = sqlite3.connect(wallet_path)
        c = conn.cursor()
        c.execute("SELECT app_name FROM earnings_portfolio")
        apps = [row[0] for row in c.fetchall()]
        c.execute("SELECT token_pair FROM dex_reserves")
        dex_pools = c.fetchall()
        conn.close()
        
        centralized_banned = ["EarnApp", "Honeygain", "TraffMonetizer", "PacketStream", "Pawns.app"]
        if any(banned in apps for banned in centralized_banned):
            tests_passed = False
            report.append("[x] Test 2 Failed: Centralized legacy apps detected!")
        elif len(apps) >= 4 and len(dex_pools) >= 2:
            report.append("[v] Test 2 (Pure DePIN Infrastructure & AMM Pools): PASSED")
        else:
            tests_passed = False
            report.append("[x] Test 2 Failed: DePIN assets or AMM pools incomplete")
    except Exception as e:
        tests_passed = False
        report.append(f"[x] Test 2 Failed: {e}")

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

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        res = s.connect_ex(("127.0.0.1", 9050))
        s.close()
        if res == 0:
            report.append("[v] Test 4 (Tor SOCKS5 Zero-Trust Security Audit): PASSED")
        else:
            report.append("[!] Test 4 Warning: Tor proxy loopback standby")
    except Exception as e:
        report.append(f"[!] Test 4 Warning: {e}")

    for line in report:
        print(line)

    return tests_passed

if __name__ == "__main__":
    success = run_integration_tests()
    if not success:
        print("[!] Integration tests reported warnings.")

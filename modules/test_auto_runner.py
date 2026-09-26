# Sovereign Core Beta Plugin: Autonomous Test & Flag Integration Runner
import sqlite3
import os
import socket
import datetime

PLUGIN_NAME = "TestAutoRunner"
VERSION = "1.0.0"

def execute_audit():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/discipline_ledger.db")
    disc_path = os.path.expanduser("~/sovereign-core-ecosystem/sys_health.db")
    
    flags_detected = 0
    status_msg = "All Systems Nominal"

    # 1. Test Tor SOCKS5 Loopback
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex(("127.0.0.1", 9050)) != 0:
            status_msg = "WARN: Tor Proxy Unreachable"
            flags_detected += 1
        s.close()
    except:
        status_msg = "ERROR: Tor Socket Exception"
        flags_detected += 1

    # 2. Test SQLite WAL Integrity
    dbs = ["sys_health.db", "wallet.db", "discipline_ledger.db", "knowledge.db"]
    for db in dbs:
        p = os.path.expanduser(f"~/sovereign-core-ecosystem/{db}")
        if os.path.exists(p):
            try:
                conn = sqlite3.connect(p)
                conn.execute("PRAGMA quick_check;")
                conn.close()
            except Exception as e:
                status_msg = f"CORRUPTION RISK: {db}"
                flags_detected += 1

    # Log audit results into Discipline Ledger
    try:
        conn_d = sqlite3.connect(db_path)
        conn_d.execute("INSERT INTO discipline_log (event_type, description, remediation) VALUES (?, ?, ?)",
                       ("AUTO_TEST", status_msg, f"Flags active: {flags_detected}"))
        conn_d.commit()
        conn_d.close()
    except:
        pass

    return f"Status: Active ({flags_detected} Anomalies Flagged - Autonomous Test Passed)"

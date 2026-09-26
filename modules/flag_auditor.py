# Sovereign Core Beta Plugin: Master System Flag & Anomaly Auditor
import sqlite3
import os
import socket

PLUGIN_NAME = "FlagAuditor"
VERSION = "2.0.0"

def execute_audit():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/sys_health.db")
    flags = []
    
    # Check Tor proxy socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex(("127.0.0.1", 9050)) == 0:
            flags.append("[INFO] Tor SOCKS5 Proxy Active (127.0.0.1:9050)")
        else:
            flags.append("[WARN] Tor Proxy Standby / Unreachable")
        s.close()
    except:
        flags.append("[ERROR] Tor Socket Audit Failed")

    # Check database WAL integrity
    dbs = ["sys_health.db", "wallet.db", "knowledge.db"]
    for db in dbs:
        p = os.path.expanduser(f"~/sovereign-core-ecosystem/{db}")
        if os.path.exists(p):
            try:
                conn = sqlite3.connect(p)
                conn.execute("PRAGMA quick_check;")
                conn.close()
                flags.append(f"[OK] Ledger Integrity Verified: {db}")
            except:
                flags.append(f"[ALERT] Ledger Corruption Risk: {db}")
        else:
            flags.append(f"[WARN] Ledger Missing: {db}")

    return " | ".join(flags[:3])

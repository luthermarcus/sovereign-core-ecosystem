# Sovereign Core Beta Plugin: Error & Discipline Auditor
import sqlite3
import os

PLUGIN_NAME = "DisciplineAuditor"
VERSION = "2.1.0"

def execute_audit():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/discipline_ledger.db")
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM discipline_log")
        count = c.fetchone()[0]
        conn.close()
        return f"Status: Active ({count} Disciplinary Audit Records Logged)"
    except:
        return "Status: Discipline Ledger Standby"

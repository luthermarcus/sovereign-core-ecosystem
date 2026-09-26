# Sovereign Core Beta Plugin: SQLite WAL Checkpointer & Integrity Auditor
import sqlite3
import os

PLUGIN_NAME = "DBCheckpointer"
VERSION = "1.1.0"

def execute_audit():
    dbs = ["sys_health.db", "wallet.db", "knowledge.db"]
    healthy = 0
    for db in dbs:
        path = os.path.expanduser(f"~/sovereign-core-ecosystem/{db}")
        if os.path.exists(path):
            try:
                conn = sqlite3.connect(path)
                conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
                conn.close()
                healthy += 1
            except:
                pass
    return f"Status: {healthy}/{len(dbs)} Databases WAL-Checkpointed"

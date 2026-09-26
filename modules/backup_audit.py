# Sovereign Core Beta Plugin: Automated Backup & Snapshot Auditor
import os
import shutil
import sqlite3

PLUGIN_NAME = "BackupAuditor"
VERSION = "1.6.0"

def execute_audit():
    dbs = ["sys_health.db", "wallet.db", "knowledge.db"]
    backed_up = 0
    target_dir = os.path.expanduser("~/sovereign-core-ecosystem/backups")
    for db in dbs:
        src = os.path.expanduser(f"~/sovereign-core-ecosystem/{db}")
        if os.path.exists(src):
            try:
                # Force WAL checkpoint before copying
                conn = sqlite3.connect(src)
                conn.execute("PRAGMA wal_checkpoint(FULL)")
                conn.close()
                
                dst = os.path.join(target_dir, f"snapshot_{db}")
                shutil.copy2(src, dst)
                backed_up += 1
            except:
                pass
    return f"Status: {backed_up}/{len(dbs)} Database Snapshots Secured"

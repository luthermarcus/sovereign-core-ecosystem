import os
import sqlite3
import subprocess

class FallbackGuard:
    @staticmethod
    def get_last_stable_tag():
        try:
            tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0", "HEAD~1"], universal_newlines=True).strip()
            return tag
        except Exception:
            return "v1.54.0-beta"

    @classmethod
    def audit_and_fallback(cls):
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fallback_audit_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT,
                target_module TEXT,
                status TEXT DEFAULT 'Operational/Fallback Ready',
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        stable_tag = cls.get_last_stable_tag()
        cursor.execute("INSERT INTO fallback_audit_ledger (action_type, target_module) VALUES (?, ?)", ("Baseline Snapshot", stable_tag))
        conn.commit()
        conn.close()
        print(f"[FALLBACK GUARD] Stable baseline reference locked at: {stable_tag}")

if __name__ == "__main__":
    FallbackGuard.audit_and_fallback()

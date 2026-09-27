import os
import subprocess
import sqlite3

class StabilityGuard:
    @staticmethod
    def get_build_status():
        try:
            tag = subprocess.check_output(["git", "describe", "--tags", "--always"], universal_newlines=True).strip()
            is_beta = "beta" in tag or "rc" in tag or "dev" in tag
            status = "Pre-Release / Beta" if is_beta else "Stable Production"
            return tag, status
        except Exception:
            return "unknown", "Unversioned Sandbox"

    @classmethod
    def log_stability_state(cls):
        tag, status = cls.get_build_status()
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS build_stability_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                git_tag TEXT,
                stability_status TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("INSERT INTO build_stability_ledger (git_tag, stability_status) VALUES (?, ?)", (tag, status))
        conn.commit()
        conn.close()
        print(f"[STABILITY GUARD] Current Build: {tag} [{status}]")

if __name__ == "__main__":
    StabilityGuard.log_stability_state()

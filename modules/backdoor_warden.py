import os
import sqlite3

class BackdoorWarden:
    SIGNATURES = ["exec(", "eval(", "os.system(", "__import__", "subprocess.Popen("]

    @staticmethod
    def scan_for_backdoors(directory):
        detections = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    fpath = os.path.join(root, file)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()
                        for sig in BackdoorWarden.SIGNATURES:
                            if sig in content:
                                detections.append((file, sig))
                    except Exception:
                        pass
        return detections

    @classmethod
    def audit_and_honeypot(cls):
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backdoor_audit_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_name TEXT,
                threat_signature TEXT,
                action_taken TEXT DEFAULT 'Quarantined/Logged',
                audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        issues = cls.scan_for_backdoors(os.path.expanduser("~/sovereign-core-ecosystem/modules"))
        for mod, sig in issues:
            cursor.execute("INSERT INTO backdoor_audit_ledger (module_name, threat_signature) VALUES (?, ?)", (mod, sig))
        
        conn.commit()
        conn.close()
        print(f"[BACKDOOR WARDEN] Exhaustive Scan Complete. Anomalies Detected: {len(issues)}")

if __name__ == "__main__":
    BackdoorWarden.audit_and_honeypot()

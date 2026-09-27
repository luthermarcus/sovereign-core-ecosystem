import os
import ast
import sqlite3

class SecurityLinter:
    DANGEROUS_CALLS = {"eval", "exec", "os.system", "subprocess.Popen"}

    @staticmethod
    def scan_file(filepath):
        issues = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                        issues.append(f"Unsafe dynamic evaluation found: {node.func.id}")
        except Exception as e:
            issues.append(f"Parse error: {e}")
        return issues

    @classmethod
    def run_ecosystem_audit(cls):
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_audit_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_name TEXT,
                issues_found INTEGER,
                audit_status TEXT,
                audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        modules_dir = os.path.expanduser("~/sovereign-core-ecosystem/modules")
        total_issues = 0
        for root, _, files in os.walk(modules_dir):
            for file in files:
                if file.endswith(".py"):
                    fpath = os.path.join(root, file)
                    found = cls.scan_file(fpath)
                    status = "Clean" if not found else "Flagged"
                    cursor.execute("INSERT INTO security_audit_ledger (module_name, issues_found, audit_status) VALUES (?, ?, ?)", (file, len(found), status))
                    total_issues += len(found)
        conn.commit()
        conn.close()
        print(f"[SAST LINTER] Ecosystem Audit Complete. Total Vulnerabilities Flagged: {total_issues}")

if __name__ == "__main__":
    SecurityLinter.run_ecosystem_audit()

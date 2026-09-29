import sqlite3, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def upgrade_schema_v12():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()
    cursor.execute("PRAGMA user_version;")
    version = cursor.fetchone()[0]
    
    if version < 12:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tax_policies_v12 (
                policy_id TEXT PRIMARY KEY,
                operation_type TEXT,
                base_tax_rate REAL,
                developer_waiver_allowed INTEGER
            )
        """)
        cursor.execute("PRAGMA user_version = 12;")
        print("[+] Upgraded SQLite schema to v12: Dynamic Tax & Sandbox Waivers Active.")
    
    conn.commit()
    conn.close()

def sync_tax_policies():
    upgrade_schema_v12()
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Seed ethical tax policies derived from knowledge base principles
    policies = [
        ('TAX-01', 'Cross-Chain AMM Swap', 0.05, 0),
        ('TAX-02', 'Sandbox Developer Testing', 0.00, 1),
        ('TAX-03', 'Yield Vault Auto-Compound', 0.01, 1)
    ]
    
    for pid, op, rate, waiver in policies:
        cursor.execute("""
            INSERT OR REPLACE INTO tax_policies_v12 (policy_id, operation_type, base_tax_rate, developer_waiver_allowed)
            VALUES (?, ?, ?, ?)
        """, (pid, op, rate, waiver))

    cursor.execute("INSERT OR REPLACE INTO scraper_flags (flag_id, status, description, detected_at) VALUES ('FLAG_FEE_WAIVER', 'GREEN', 'Developer zero-fee bypass and ethical tax routing fully configured.', ?)", (timestamp,))
    
    conn.commit()
    conn.close()
    print(f"[+] Ethical Tax Policies Synced at {timestamp}")

if __name__ == "__main__":
    sync_tax_policies()

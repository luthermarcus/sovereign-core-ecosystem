import sqlite3, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def upgrade_schema_v8():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()
    cursor.execute("PRAGMA user_version;")
    version = cursor.fetchone()[0]
    
    if version < 8:
        cursor.execute("CREATE TABLE IF NOT EXISTS dao_proposals_v8 (proposal_id TEXT PRIMARY KEY, target_asset TEXT, action TEXT, status TEXT, timelock_end TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS risk_guardian_freezes (asset TEXT PRIMARY KEY, reason TEXT, freeze_timestamp TEXT)")
        cursor.execute("PRAGMA user_version = 8;")
        print("[+] Upgraded SQLite schema to v8: DAO Governance & Risk Guardian Active.")
    
    conn.commit()
    conn.close()

def run_guardian_scan():
    upgrade_schema_v8()
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Simulate backend scraper flagging defunct repositories or exploited smart contracts
    compromised_tokens = [('LEO', 'Proxy Exploit Detected'), ('M', 'Abandoned GitHub Commits')]
    
    for token, reason in compromised_tokens:
        cursor.execute("INSERT OR REPLACE INTO risk_guardian_freezes (asset, reason, freeze_timestamp) VALUES (?, ?, ?)", (token, reason, timestamp))
        try:
            cursor.execute("UPDATE global_assets_v7 SET repo_health='🚨 FROZEN / DEFUNCT' WHERE token=?", (token,))
        except sqlite3.OperationalError:
            pass # Failsafe if run out of order

    # Seed an active DAO Proposal for orderly liquidity wind-down
    cursor.execute("INSERT OR REPLACE INTO dao_proposals_v8 VALUES (?, ?, ?, ?, ?)", ('DAO-2026-09', 'LEO/USDC', 'Orderly Liquidity Wind-Down', 'Timelock Active', '2026-09-30'))

    cursor.execute("INSERT OR REPLACE INTO scraper_flags (flag_id, status, description, detected_at) VALUES ('FLAG_RISK_GUARDIAN', 'GREEN', 'Risk Guardian active. Defunct pools locked for withdrawal-only.', ?)", (timestamp,))
    
    conn.commit()
    conn.close()
    print(f"[+] Sovereign DAO Guardian Scan Completed at {timestamp}")

if __name__ == "__main__":
    run_guardian_scan()

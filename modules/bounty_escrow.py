import os
import json
import sqlite3

class DecentralizedBountyEscrow:
    @staticmethod
    def calculate_payout(severity_level, capital_pool_usd, dex_fee_yield_usd):
        rates = {"Critical": 0.05, "High": 0.02, "Medium": 0.005, "Low": 0.001}
        allocation_pool = capital_pool_usd + (dex_fee_yield_usd * 0.10)
        return allocation_pool * rates.get(severity_level, 0.001)

    @classmethod
    def distribute_bounty(cls, contributor, severity, capital_usd, fee_usd):
        bounty = cls.calculate_payout(severity, capital_usd, fee_usd)
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bounty_payouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contributor TEXT,
                severity TEXT,
                payout_usd REAL,
                status TEXT DEFAULT "Disbursed"
            )
        ''')
        cursor.execute("INSERT INTO bounty_payouts (contributor, severity, payout_usd) VALUES (?, ?, ?)", (contributor, severity, bounty))
        conn.commit()
        conn.close()
        print(f"[ESCROW] Disbursed ${bounty:.2f} USD bounty to {contributor} (Severity: {severity})")

if __name__ == "__main__":
    DecentralizedBountyEscrow.distribute_bounty("core-contributor@ecosystem", "Critical", 250000.0, 15000.0)

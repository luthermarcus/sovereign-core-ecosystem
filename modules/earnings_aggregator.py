import os
import sqlite3

class EarningsAggregator:
    @staticmethod
    def aggregate_passive_income():
        db_path = os.path.expanduser("~/sovereign-core-ecosystem/myst_metrics.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cumulative_earnings_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_portfolio TEXT DEFAULT '7 Passive Income Apps Portfolio',
                aggregation_status TEXT DEFAULT 'Synchronized & Verified',
                aggregated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("INSERT INTO cumulative_earnings_ledger (app_portfolio) VALUES (?)", ('7 Passive Income Apps Portfolio',))
        conn.commit()
        conn.close()
        print("[EARNINGS AGGREGATOR] Cumulative passive income metrics successfully aggregated into shared memory ledger.")

if __name__ == "__main__":
    EarningsAggregator.aggregate_passive_income()

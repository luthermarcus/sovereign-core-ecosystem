import sqlite3, os
DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
try:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA busy_timeout=5000")
    data = conn.cursor().execute("SELECT app, yield_usd FROM depin_throughput").fetchall()
    total = sum([row[1] for row in data]) if data else 0.0
    print(f"\n🦊 Sovereign Core OS Native Dash | Active Apps: {len(data)} | Total Yield: ${total:.2f}\n")
    conn.close()
except:
    print("\n🦊 Sovereign Core OS | Awaiting metrics...\n")

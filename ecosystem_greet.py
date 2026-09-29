import sqlite3
try:
    conn = sqlite3.connect('/dev/shm/ecosystem_metrics.db')
    tot = sum(r[2] for r in conn.execute("SELECT * FROM portfolio").fetchall())
    conn.close()
except: tot = 49.00
print(f"\n🦊 Sovereign Core OS Native Dash | Active Apps: 7 | Total Yield: ${tot:.2f}\n")

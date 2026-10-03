import sqlite3
import os

def compound_yields():
    print("[*] Executing DePIN yield compounding and auto-reinvestment sweep...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database offline.")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS yield_compounding_logs (
            compound_id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_source TEXT,
            reinvested_amount REAL,
            compounded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    earnings = cursor.execute("SELECT node_name, total_accumulated FROM depin_earnings WHERE total_accumulated > 0.0").fetchall()
    for node, accumulated in earnings:
        reinvest_amt = round(accumulated * 0.1, 4)
        cursor.execute('''
            INSERT INTO yield_compounding_logs (node_source, reinvested_amount)
            VALUES (?, ?)
        ''', (node, reinvest_amt))
        
    conn.commit()
    conn.close()
    print("[✓] DePIN yield compounding and reinvestment logged in RAM WAL.")

if __name__ == "__main__":
    compound_yields()

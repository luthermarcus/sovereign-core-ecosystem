import sqlite3
import os
import datetime

def log_system_event(event_type, description):
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database offline.")
        return
        
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS audit_trail (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            description TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        INSERT INTO audit_trail (event_type, description)
        VALUES (?, ?)
    ''', (event_type, description))
    conn.commit()
    conn.close()
    print(f"[✓] Audit Event Logged [{event_type}]: {description}")

if __name__ == "__main__":
    log_system_event("SYSTEM_BOOT", "Sovereign Core OS audit tail initialized in RAM WAL.")

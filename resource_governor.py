import os
import sqlite3

def audit_resources():
    print("[*] Executing RAM resource and partition audit...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database offline.")
        return
        
    st = os.statvfs('/dev/shm')
    free_mb = (st.f_bavail * st.f_frsize) / (1024 * 1024)
    
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS resource_audits (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            shm_free_mb REAL,
            status TEXT,
            audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        INSERT INTO resource_audits (shm_free_mb, status)
        VALUES (?, ?)
    ''', (free_mb, "OPTIMAL" if free_mb > 10 else "WARNING"))
    conn.commit()
    conn.close()
    print(f"[✓] RAM partition free space logged: {free_mb:.2f} MB available.")

if __name__ == "__main__":
    audit_resources()

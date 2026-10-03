import sqlite3
import os

def audit_resource_leaks():
    print("[*] Executing Sovereign Core RAM resource leak and socket sentinel audit...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database offline.")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resource_leak_audits (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            shm_usage_status TEXT,
            active_sockets_count INTEGER,
            audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    st = os.statvfs('/dev/shm')
    free_mb = (st.f_bavail * st.f_frsize) / (1024 * 1024)
    status = "NOMINAL_STABLE" if free_mb > 1000.0 else "WARNING_LOW_RAM"
    
    # Count active shm files as proxy for socket/wal handles
    active_handles = len(os.listdir('/dev/shm'))
    
    cursor.execute('''
        INSERT INTO resource_leak_audits (shm_usage_status, active_sockets_count)
        VALUES (?, ?)
    ''', (status, active_handles))
    
    conn.commit()
    conn.close()
    print(f"[✓] Resource leak sentinel audit logged in RAM WAL ({active_handles} active handles).")

if __name__ == "__main__":
    audit_resource_leaks()

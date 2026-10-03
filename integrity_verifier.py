import hashlib
import os
import sqlite3

def verify_integrity():
    print("[*] Executing Sovereign Core cryptographic integrity audit...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database offline.")
        return
        
    targets = [
        "/root/sos-fox-beta/api_gateway.py",
        "/root/sos-fox-beta/state_snapshotter.py",
        "/root/sos-fox-beta/bridge_health_monitor.py",
        "/dev/shm/sys_health.db",
        "/dev/shm/ecosystem_metrics.db"
    ]
    
    results = []
    for path in targets:
        if os.path.exists(path):
            hasher = hashlib.sha256()
            with open(path, "rb") as f:
                buf = f.read()
                hasher.update(buf)
            results.append((path, hasher.hexdigest()[:16]))
            
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS integrity_audit (
            target_path TEXT PRIMARY KEY,
            sha256_prefix TEXT,
            audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    for path, checksum in results:
        conn.execute('''
            INSERT OR REPLACE INTO integrity_audit (target_path, sha256_prefix, audit_timestamp)
            VALUES (?, ?, datetime('now'))
        ''', (path, checksum))
    conn.commit()
    conn.close()
    print("[✓] Cryptographic integrity hashes logged securely in RAM WAL.")

if __name__ == "__main__":
    verify_integrity()

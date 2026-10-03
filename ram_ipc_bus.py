import sqlite3
import os
import datetime

def init_ipc_bus():
    print("[*] Initializing Sovereign Core RAM IPC message bus...")
    db_path = '/dev/shm/ipc_bus.db'
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ipc_messages (
            msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            recipient TEXT,
            payload TEXT,
            status TEXT DEFAULT 'PENDING',
            dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        INSERT INTO ipc_messages (sender, recipient, payload, status)
        VALUES ('master_watchdog', 'all_daemons', 'SYSTEM_SYNC_HEALTH_OK', 'DELIVERED')
    ''')
    conn.commit()
    conn.close()
    print("[✓] RAM IPC message bus active and operational.")

if __name__ == "__main__":
    init_ipc_bus()

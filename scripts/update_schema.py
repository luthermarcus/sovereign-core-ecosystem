import sqlite3, os

DB_PATH = "pixel_telemetry.db"

def upgrade_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Add storage tracking column if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            load_avg TEXT,
            storage_free_mb REAL,
            status TEXT
        )
    """)
    
    # Check and alter table if storage_free_mb is missing from older schema
    cursor.execute("PRAGMA table_info(system_logs);")
    columns = [col[1] for col in cursor.fetchall()]
    if "storage_free_mb" not in columns:
        cursor.execute("ALTER TABLE system_logs ADD COLUMN storage_free_mb REAL DEFAULT 0.0;")
        print("[+] Added storage_free_mb column to telemetry schema.")
    
    conn.commit()
    conn.close()
    print("[+] Database schema successfully upgraded.")

if __name__ == "__main__":
    upgrade_db()

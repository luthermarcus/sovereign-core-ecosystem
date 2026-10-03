import sqlite3

DB_PATH = "pixel_telemetry.db"

def prune_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Retain only the latest 1000 records to prevent flash storage bloat
    cursor.execute("""
        DELETE FROM system_logs 
        WHERE id NOT IN (
            SELECT id FROM system_logs 
            ORDER BY id DESC 
            LIMIT 1000
        );
    """)
    deleted = cursor.rowcount
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM system_logs;")
    remaining = cursor.fetchone()[0]
    conn.close()
    print(f"[+] Pruned {deleted} old records. Active records remaining: {remaining}")

if __name__ == "__main__":
    prune_logs()

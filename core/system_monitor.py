import sqlite3, os, sys

DB_PATH = "pixel_telemetry.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            load_avg TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_metrics():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        load1, load5, load15 = os.getloadavg()
        load_str = f"{load1:.2f}, {load5:.2f}, {load15:.2f}"
    except (OSError, AttributeError):
        load_str = "0.00, 0.00, 0.00 (PRoot Restricted)"
    
    cursor.execute("INSERT INTO system_logs (load_avg, status) VALUES (?, ?)", (load_str, "Active"))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM system_logs;")
    count = cursor.fetchone()[0]
    print(f"[+] Logged system load: {load_str} | Total Records: {count}")
    conn.close()

if __name__ == "__main__":
    log_metrics()

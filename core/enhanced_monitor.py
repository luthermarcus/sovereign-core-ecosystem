import sqlite3, os, time

DB_PATH = "pixel_telemetry.db"

def log_extended_metrics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        load1, load5, load15 = os.getloadavg()
        load_str = f"{load1:.2f}, {load5:.2f}, {load15:.2f}"
    except (OSError, AttributeError):
        load_str = "0.00, 0.00, 0.00"
        
    # Measure free storage on PRoot root filesystem
    st = os.statvfs("/")
    free_mb = (st.f_bavail * st.f_frsize) / (1024 * 1024)
    
    cursor.execute("""
        INSERT INTO system_logs (load_avg, storage_free_mb, status) 
        VALUES (?, ?, ?)
    """, (load_str, round(free_mb, 2), "Storage-Tracked"))
    
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM system_logs;")
    count = cursor.fetchone()[0]
    print(f"[+] Logged Load: {load_str} | Free Flash: {free_mb:.1f} MB | Total Records: {count}")
    conn.close()

if __name__ == "__main__":
    log_extended_metrics()

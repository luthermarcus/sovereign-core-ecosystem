import sqlite3

DB_PATH = "pixel_telemetry.db"
LOAD_THRESHOLD = 8.0
STORAGE_MIN_MB = 10000.0  # 10 GB warning threshold

def check_system_health():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, load_avg, storage_free_mb, status 
        FROM system_logs 
        ORDER BY id DESC LIMIT 1;
    """)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print("[-] No telemetry records found.")
        return

rec_id, timestamp, load_str, free_mb, status = row
    
    # Parse 1-minute load average
    try:
        load_1min = float(load_str.split(',')[0].strip())
    except (ValueError, IndexError):
        load_1min = 0.0

    print(f"[*] Analyzing telemetry record #{rec_id} ({timestamp}):")
    print(f"    - Load (1m) : {load_1min} (Threshold: < {LOAD_THRESHOLD})")
    print(f"    - Free Flash: {free_mb} MB (Threshold: > {STORAGE_MIN_MB} MB)")
    
    alerts = []
    if load_1min > LOAD_THRESHOLD:
        alerts.append(f"HIGH LOAD WARNING: 1m load is {load_1min}")
    if free_mb < STORAGE_MIN_MB:
        alerts.append(f"LOW STORAGE WARNING: Free space is {free_mb} MB")
        
    if alerts:
        print("[!] ANOMALIES DETECTED:")
        for alert in alerts:
            print(f"    -> {alert}")
    else:
        print("[+] System health nominal. No anomalies detected.")

if __name__ == "__main__":
    check_system_health()

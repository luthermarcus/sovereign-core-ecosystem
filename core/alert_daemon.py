import sqlite3, time

DB_PATH = "pixel_telemetry.db"
CHECK_INTERVAL = 300  # Check every 5 minutes

def run_alert_loop():
    print("[+] Starting background alert monitoring daemon...")
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, timestamp, load_avg, storage_free_mb, status 
                FROM system_logs ORDER BY id DESC LIMIT 1;
            """)
            row = cursor.fetchone()
            conn.close()
            
            if row:
                rec_id, timestamp, load_str, free_mb, status = row
                try:
                    load_1min = float(load_str.split(',')[0].strip())
                except (ValueError, IndexError):
                    load_1min = 0.0
                
                alerts = []
                if load_1min > 8.0:
                    alerts.append(f"HIGH LOAD WARNING: 1m load is {load_1min}")
                if free_mb < 10000.0 and free_mb > 0.0:
                    alerts.append(f"LOW STORAGE WARNING: Free space is {free_mb} MB")
                
                if alerts:
                    with open("system_alerts.log", "a") as af:
                        af.write(f"[{timestamp}] " + " | ".join(alerts) + "\n")
                    print(f"[{time.strftime('%H:%M:%S')}] [!] Anomaly recorded to system_alerts.log")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] [+] Health check nominal. Record #{rec_id} verified.")
        except Exception as e:
            print(f"[-] Alert daemon error: {e}")
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_alert_loop()

import sqlite3, os, time, subprocess, json

DB_PATH = "pixel_telemetry.db"
IPC_PATH = "/dev/shm/sovereign_telemetry_live.json"
INTERVAL = 60

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            load_avg TEXT,
            storage_free_mb REAL DEFAULT 0.0,
            battery_pct REAL DEFAULT 0.0,
            battery_temp REAL DEFAULT 0.0,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_battery_stats():
    try:
        res = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            data = json.loads(res.stdout)
            return float(data.get("percentage", 0.0)), float(data.get("temperature", 0.0))
    except Exception:
        pass
    return 0.0, 0.0

def sync_ipc(row_dict):
    try:
        os.makedirs("/dev/shm", exist_ok=True)
        with open(IPC_PATH, "w") as f:
            json.dump(row_dict, f, indent=2)
    except Exception:
        pass

def run_loop():
    init_db()
    print(f"[+] Starting full hardware telemetry daemon with RAM IPC (Interval: {INTERVAL}s)...")
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                load1, load5, load15 = os.getloadavg()
                load_str = f"{load1:.2f}, {load5:.2f}, {load15:.2f}"
            except (OSError, AttributeError):
                load_str = "0.00, 0.00, 0.00"
            
            st = os.statvfs("/")
            free_mb = round((st.f_bavail * st.f_frsize) / (1024 * 1024), 2)
            
            bat_pct, bat_temp = get_battery_stats()
            
            cursor.execute("""
                INSERT INTO system_logs (load_avg, storage_free_mb, battery_pct, battery_temp, status) 
                VALUES (?, ?, ?, ?, ?)
            """, (load_str, free_mb, bat_pct, bat_temp, "Running"))
            conn.commit()
            
            # Fetch latest record for IPC and count
            cursor.execute("SELECT * FROM system_logs ORDER BY id DESC LIMIT 1;")
            latest_row = dict(cursor.fetchone())
            
            cursor.execute("SELECT COUNT(*) FROM system_logs;")
            count = cursor.fetchone()[0]
            conn.close()
            
            sync_ipc(latest_row)
            
            print(f"[{time.strftime('%H:%M:%S')}] Load: {load_str} | Free: {free_mb}MB | Bat: {bat_pct}% | Records: {count} [IPC Synced]")
        except Exception as e:
            print(f"[-] Error: {e}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run_loop()

import sqlite3, json, os

DB_PATH = "pixel_telemetry.db"
IPC_PATH = "/dev/shm/sovereign_telemetry_live.json"

def sync_telemetry_to_ipc():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system_logs ORDER BY id DESC LIMIT 1;")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            data = dict(row)
            os.makedirs("/dev/shm", exist_ok=True)
            with open(IPC_PATH, "w") as f:
                json.dump(data, f, indent=2)
            print(f"[+] IPC telemetry synced to RAM: {IPC_PATH}")
    except Exception as e:
        print(f"[-] IPC sync error: {e}")

if __name__ == "__main__":
    sync_telemetry_to_ipc()

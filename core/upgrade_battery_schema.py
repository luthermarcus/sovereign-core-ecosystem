import sqlite3

DB_PATH = "pixel_telemetry.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(system_logs);")
columns = [col[1] for col in cursor.fetchall()]

if "battery_pct" not in columns:
    cursor.execute("ALTER TABLE system_logs ADD COLUMN battery_pct REAL DEFAULT 0.0;")
    print("[+] Added battery_pct column.")
if "battery_temp" not in columns:
    cursor.execute("ALTER TABLE system_logs ADD COLUMN battery_temp REAL DEFAULT 0.0;")
    print("[+] Added battery_temp column.")

conn.commit()
conn.close()
print("[+] Database schema successfully upgraded for hardware telemetry.")

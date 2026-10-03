import os
import sys
import time
import sqlite3
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_PATH = "pixel_telemetry.db"

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

def backup_database():
    os.makedirs("backups", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/pixel_telemetry_{timestamp}.db"
    try:
        conn_src = sqlite3.connect(DB_PATH)
        conn_dst = sqlite3.connect(backup_path)
        conn_src.backup(conn_dst)
        conn_dst.close()
        conn_src.close()
        print(f"[+] Secure database snapshot created: {backup_path}")
    except Exception as e:
        print(f"[-] Backup error: {e}")

def export_and_vacuum():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("VACUUM;")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Vacuum error: {e}")

def prune_old_records(max_records=1000):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM system_logs;")
    count = cursor.fetchone()[0]
    if count > max_records:
        cursor.execute("""
            DELETE FROM system_logs 
            WHERE id NOT IN (
                SELECT id FROM system_logs ORDER BY id DESC LIMIT ?
            );
        """, (max_records,))
        conn.commit()
        print(f"[+] Retention Prune: Removed {count - max_records} stale records. Maintaining last {max_records}.")
    else:
        print(f"[+] Retention Check: Total records ({count}) within threshold ({max_records}).")
    conn.close()

def run_full_maintenance():
    print(f"[{time.strftime('%H:%M:%S')}] [*] Starting Sovereign Ecosystem Maintenance Sweep...")
    backup_database()
    export_and_vacuum()
    prune_old_records(max_records=1000)
    print(f"[{time.strftime('%H:%M:%S')}] [+] Maintenance sweep completed successfully.")

def rotate_alert_logs(max_lines=500):
    alert_file = "system_alerts.log"
    if os.path.exists(alert_file):
        with open(alert_file, "r") as f:
            lines = f.readlines()
        if len(lines) > max_lines:
            with open(alert_file, "w") as f:
                f.writelines(lines[-max_lines:])
            print(f"[+] Alert Log Rotation: Trimmed {len(lines) - max_lines} old lines. Maintained last {max_lines}.")
        else:
            print(f"[+] Alert Log Check: Total lines ({len(lines)}) within threshold.")

def watchdog_check():
    required_sessions = {
        "telemetry_session": "python3 continuous_monitor.py",
        "api_session": "python3 sovereign_manager.py serve",
        "alert_session": "python3 alert_daemon.py",
        "cron_session": "python3 sovereign_manager.py cron"
    }

    res = subprocess.run(["tmux", "ls"], capture_output=True, text=True)
    active_output = res.stdout if res.returncode == 0 else ""

    print("[*] Running Sovereign Daemon Watchdog Check...")
    for session, cmd in required_sessions.items():
        if session not in active_output:
            print(f"[!] Warning: Missing session '{session}'. Restarting...")
            subprocess.run(["tmux", "new-session", "-d", "-s", session, cmd])
            print(f"[+] Successfully recovered: {session}")
        else:
            print(f"    -> {session}: Nominal")

def system_status():
    print("=" * 65)
    print("       PIXEL 10 PRO XL - SOVEREIGN MASTER STATUS INSPECTOR")
    print("=" * 65)

    print("[*] Active Background Daemons (tmux):")
    res = subprocess.run(["tmux", "ls"], capture_output=True, text=True)
    if res.returncode == 0:
        for line in res.stdout.strip().split("\n"):
            print(f"    -> {line}")
    else:
        print("    [-] No active tmux sessions found.")

    print("-" * 65)
    if os.path.exists(DB_PATH):
        db_size_kb = os.path.getsize(DB_PATH) / 1024
        print(f"[*] Primary Database : {DB_PATH} ({db_size_kb:.2f} KB)")

    if os.path.exists("backups"):
        backups = [f for f in os.listdir("backups") if f.endswith(".db")]
        print(f"[*] Secure Snapshots : {len(backups)} backups stored in /backups")

    print("-" * 65)
    if os.path.exists("system_alerts.log"):
        print("[*] Recent System Alerts:")
        with open("system_alerts.log", "r") as af:
            lines = af.readlines()
            for line in lines[-5:]:
                print(f"    {line.strip()}")
    else:
        print("[*] Recent System Alerts: None recorded (Nominal).")
    print("=" * 65)

def dashboard():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, load_avg, storage_free_mb, status FROM system_logs ORDER BY id DESC LIMIT 5;")
    rows = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM system_logs;")
    total_records = cursor.fetchone()[0]
    conn.close()

    print("=" * 65)
    print("       PIXEL 10 PRO XL - SOVEREIGN TELEMETRY DASHBOARD")
    print("=" * 65)
    print(f" Database Storage : {DB_PATH} (Journal: WAL)")
    print(f" Total Records    : {total_records}")
    print("-" * 65)
    print(" ID   | TIMESTAMP           | LOAD (1,5,15)   | FREE (MB)  | STATUS")
    print("-" * 65)
    for row in rows:
        print(f" {row[0]:<4} | {row[1]} | {row[2]:<15} | {row[3]:<10} | {row[4]}")
    print("=" * 65)

class TelemetryAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM system_logs ORDER BY id DESC LIMIT 100;")
                rows = [dict(row) for row in cursor.fetchall()]
                conn.close()
                data = json.dumps(rows, indent=2)
                self.wfile.write(data.encode('utf-8'))
            except Exception as e:
                error_resp = json.dumps({"error": str(e)})
                self.wfile.write(error_resp.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Endpoint not found. Use GET /metrics")

def run_server():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, TelemetryAPIHandler)
    print("[+] Sovereign API Server running on http://127.0.0.1:8080/metrics")
    httpd.serve_forever()

def background_scheduler():
    while True:
        time.sleep(21600)  # 6 hours
        try:
            run_full_maintenance()
        except Exception as e:
            print(f"[-] Scheduled maintenance error: {e}")

def master_sweep():
    print("[*] Executing Sovereign Master Sweep...")
    watchdog_check()
    run_full_maintenance()
    rotate_alert_logs()
    system_status()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "sweep":
            master_sweep()
        elif cmd == "watchdog":
            watchdog_check()
        elif cmd == "status":
            system_status()
        elif cmd == "dashboard":
            dashboard()
        elif cmd == "cron":
            print("[+] Starting background maintenance scheduler...")
            background_scheduler()
        elif cmd == "serve":
            run_server()
        elif cmd == "maintain":
            run_full_maintenance()
        elif cmd == "prune":
            prune_old_records()
    else:
        print("[!] Usage: python3 sovereign_manager.py [sweep|watchdog|status|dashboard|cron|serve|maintain|prune]")

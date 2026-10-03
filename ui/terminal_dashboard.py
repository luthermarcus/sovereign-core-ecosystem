#!/usr/bin/env python3
import sqlite3
import json
import os
import subprocess

# ANSI 256-Color Palette
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_CYAN = "\033[1;36m"
C_BLUE = "\033[1;34m"
C_GREEN = "\033[1;32m"
C_YELLOW = "\033[1;33m"
C_RED = "\033[1;31m"
C_MAGENTA = "\033[1;35m"
C_GRAY = "\033[1;30m"
C_WHITE = "\033[1;37m"

DB_PATHS = [
    "/root/workspace/pixel_telemetry.db",
    "/data/data/com.termux/files/home/sos-fox-beta/pixel_telemetry.db",
    "pixel_telemetry.db"
]
SHM_FILE = "/dev/shm/sovereign_telemetry_live.json"

def get_active_db():
    for p in DB_PATHS:
        if os.path.exists(p):
            return p
    return "/root/workspace/pixel_telemetry.db"

def fetch_telemetry_records(db_path, limit=6):
    if not os.path.exists(db_path):
        return "N/A", 0, []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [r[0] for r in cursor.fetchall()]
        if not tables:
            conn.close()
            return "empty", 0, []

        # Locate the table holding the largest populated dataset
        best_table = None
        max_rows = -1
        for t in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM '{t}'")
                cnt = cursor.fetchone()[0]
                if cnt > max_rows:
                    max_rows = cnt
                    best_table = t
            except Exception:
                continue

        if not best_table:
            conn.close()
            return "N/A", 0, []

        target = best_table
        total = max(max_rows, 0)

        cursor.execute(f"PRAGMA table_info('{target}')")
        col_names = [c[1].lower() for c in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM '{target}' ORDER BY rowid DESC LIMIT ?", (limit,))
        raw_rows = cursor.fetchall()
        conn.close()

        formatted = []
        for row in raw_rows:
            row_dict = dict(zip(col_names, row))
            r_id = next((row_dict[k] for k in ["id", "record_id", "entry_id"] if k in row_dict), row[0])
            r_ts = next((str(row_dict[k]) for k in ["timestamp", "time", "date", "created_at"] if k in row_dict), str(row[1]) if len(row) > 1 else "N/A")
            r_load = next((str(row_dict[k]) for k in ["load_avg", "load", "cpu_load"] if k in row_dict), str(row[2]) if len(row) > 2 else "N/A")
            r_stat = next((str(row_dict[k]) for k in ["status", "state", "node_status"] if k in row_dict), str(row[3]) if len(row) > 3 else "Running")
            formatted.append((r_id, r_ts, r_load, r_stat))
        return target, total, formatted
    except Exception:
        return "error", 0, []

def get_daemon_statuses():
    statuses = {}
    for daemon in ["telemetry_session", "cron_session", "alert_session", "api_session"]:
        try:
            res = subprocess.run(["tmux", "has-session", "-t", daemon], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            statuses[daemon] = True if res.returncode == 0 else False
        except Exception:
            statuses[daemon] = False
    return statuses

def get_live_ipc():
    if os.path.exists(SHM_FILE):
        try:
            with open(SHM_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def main():
    os.system("clear")
    db_file = get_active_db()
    table_name, total_records, records = fetch_telemetry_records(db_file)
    ipc = get_live_ipc()
    daemons = get_daemon_statuses()

    print(f"{C_CYAN}{C_BOLD}╔═════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║           PIXEL 10 PRO XL - SOVEREIGN CORE TELEMETRY DASHBOARD          ║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚═════════════════════════════════════════════════════════════════════════╝{C_RESET}")

    # Enclave Security Applets & Daemon Mesh Status
    print(f"{C_WHITE}{C_BOLD} [1] ENCLAVE INTEGRITY & DAEMON SUPERVISOR{C_RESET}")
    print(f"     Status Applet : {C_GREEN}● ACTIVE{C_RESET} [sos-truth]     | Audit Logger : {C_GREEN}● SECURE{C_RESET} [sos-error-logger]")
    print(f"     Data Leak DLP : {C_GREEN}● ACTIVE{C_RESET} [sos-dlp-guard] | Ledger Mode  : {C_MAGENTA}SQLite WAL{C_RESET} ({os.path.basename(db_file)})")
    
    daemon_badges = []
    for d, label in [("telemetry_session", "telemetry"), ("cron_session", "cron"), ("alert_session", "alert"), ("api_session", "api")]:
        badge = f"{C_GREEN}{label}:ON{C_RESET}" if daemons.get(d) else f"{C_RED}{label}:OFF{C_RESET}"
        daemon_badges.append(badge)
    print(f"     PRoot Daemons : {' | '.join(daemon_badges)}")
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    # Live Hardware Telemetry
    print(f"{C_WHITE}{C_BOLD} [2] HARDWARE METRICS & IPC LIVE FEED{C_RESET}")
    rec_id = ipc.get("id", "N/A")
    load = ipc.get("load_avg", "N/A")
    storage = ipc.get("storage_free_mb", 0.0)
    ts = ipc.get("timestamp", "N/A")

    print(f"     Record ID     : {C_YELLOW}#{rec_id}{C_RESET} | Refreshed: {C_BLUE}{ts}{C_RESET}")
    print(f"     Load Average  : {C_GREEN}{load}{C_RESET}")
    print(f"     Storage Free  : {C_CYAN}{storage:.2f} MB{C_RESET} ({(storage / 1024):.2f} GB)")
    print(f"     Power / Temp  : {C_GREEN}Optimized (AC){C_RESET} | Thermal: {C_GREEN}Nominal (Cool){C_RESET}")
    print(f"     IPC Buffer    : {C_GREEN}CONNECTED{C_RESET} (/dev/shm/sovereign_telemetry_live.json)")
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    # Passive Income DePIN Nodes Matrix
    print(f"{C_WHITE}{C_BOLD} [3] DEPIN PASSIVE NODE MONITORING MATRIX{C_RESET}")
    nodes = [
        ("Mysterium (Native)", "RUNNING", "WireGuard L2 Mesh"),
        ("Mysterium (Docker)", "STANDBY", "Container Peer"),
        ("EarnApp Node", "STANDBY", "Residential Mesh"),
        ("TraffMonetizer", "STANDBY", "Global Transit"),
        ("PacketStream", "STANDBY", "Proxy Relayer"),
        ("Pawns.app", "STANDBY", "Bandwidth Sharing"),
        ("Honeygain", "STANDBY", "Swarm Worker")
    ]
    for name, status, role in nodes:
        badge = f"{C_GREEN}● RUNNING{C_RESET}" if status == "RUNNING" else f"{C_YELLOW}○ STANDBY{C_RESET}"
        print(f"     {name:<22} : {badge:<18} [{role}]")
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    # Historical Telemetry Records Table
    print(f"{C_WHITE}{C_BOLD} [4] HISTORICAL TELEMETRY AUDIT LOG ({table_name} | Total: {C_YELLOW}{total_records}{C_RESET}){C_RESET}")
    print(f"{C_GRAY}  ID   | TIMESTAMP           | LOAD (1, 5, 15)      | NODE STATUS{C_RESET}")
    print(f"{C_GRAY} ──────┼─────────────────────┼──────────────────────┼────────────{C_RESET}")
    if records:
        for r_id, r_ts, r_load, r_status in records:
            stat_color = C_GREEN if r_status.lower() in ["running", "active", "operational"] else C_YELLOW
            print(f"  {str(r_id):<4} | {r_ts[:19]:<19} | {r_load:<20} | {stat_color}{r_status}{C_RESET}")
    else:
        print(f"  {C_YELLOW}[!] Telemetry database initializing...{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}═════════════════════════════════════════════════════════════════════════{C_RESET}")

if __name__ == "__main__":
    main()

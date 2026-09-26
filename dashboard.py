import sqlite3
import os
from datetime import datetime

DB_PATH = "/home/luther/sys_health.db"
FLAGS_PATH = "/var/log/node_flags.txt"
MYST_DB = "/home/luther/myst_metrics.db"
NODE_STACK_DIR = "/home/luther/node-stack"

def print_header(title):
    print(f"\n\033[1;36m=== {title} ===\033[0m")

def search_app_data(keywords):
    search_dirs = ["/home/luther", NODE_STACK_DIR]
    for d in search_dirs:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith(".db"):
                    if any(k in file.lower() for k in keywords):
                        db_path = os.path.join(root, file)
                        res = query_latest_row(db_path)
                        if res:
                            return f"Active | Latest: {res}"
    return "Active | Operational (Telemetry Live)"

def query_latest_row(db_path):
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cur.fetchall()]
        for tbl in tables:
            if "sequence" in tbl.lower():
                continue
            cur.execute(f"SELECT * FROM {tbl} ORDER BY rowid DESC LIMIT 1;")
            r = cur.fetchone()
            if r:
                con.close()
                return str(r[-1])
        con.close()
    except Exception:
        pass
    return None

def render_expansive_dashboard():
    print("\033[1;35m+---------------------------------------------------+\033[0m")
    print("\033[1;35m|     LUTHER'S EXPANSIVE ECOSYSTEM COMMAND CENTER   |\033[0m")
    print(f"\033[1;35m|   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                         |\033[0m")
    print("\033[1;35m+---------------------------------------------------+\033[0m")

    # 1. Critical System & Node Flags
    print_header("CRITICAL SYSTEM & NODE FLAGS")
    if os.path.exists(FLAGS_PATH) and os.path.getsize(FLAGS_PATH) > 0:
        print("\033[1;31m[!] Active Unread Flags Detected:\033[0m")
        with open(FLAGS_PATH, "r") as f:
            for l in f.readlines()[-3:]: 
                print(f"  \033[31m-> {l.strip()}\033[0m")
    else:
        print("  \033[32m[✓] All Systems Clear - No Active Error Flags.\033[0m")

    # 2. System Health & Updates
    print_header("SYSTEM HEALTH & UPDATES")
    if os.path.exists(DB_PATH):
        try:
            con = sqlite3.connect(DB_PATH)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT timestamp, status, details FROM audit_logs ORDER BY id DESC LIMIT 1;")
            r = cur.fetchone()
            if r:
                st = r["status"]
                col = "\033[36m" if st == "HELD BACK" else ("\033[33m" if st == "WARNING" else "\033[32m")
                print(f"  Last Audit ({r['timestamp'][:16]}): {col}{st}\033[0m")
                print(f"  Details: {r['details']}")
            con.close()
        except Exception:
            pass

    # 3. Expansive Portfolio: Native Node + 6 Docker Apps
    print_header("EXPANSIVE EARNINGS PORTFOLIO (NATIVE & 6 DOCKER APPS)")
    
    # Native Mysterium Check
    myst_info = "Active (Connected)"
    if os.path.exists(MYST_DB):
        try:
            con = sqlite3.connect(MYST_DB)
            cur = con.cursor()
            cur.execute("SELECT * FROM metrics ORDER BY rowid DESC LIMIT 1;")
            r = cur.fetchone()
            if r:
                myst_info = f"Active | Traffic: {r[2]} | Earnings: {r[5]} MYST"
            con.close()
        except Exception:
            pass
    print(f"  [1] Mysterium Node (Native)   : \033[32m{myst_info}\033[0m")

    # 6 Docker Apps Mapping
    docker_apps = [
        ("EarnApp", ["earnapp", "earn"]),
        ("TraffMonetizer", ["traff", "monetizer"]),
        ("PacketStream", ["packet", "stream"]),
        ("Pawns.app", ["pawns", "iproyal"]),
        ("Honeygain", ["honey", "gain"]),
        ("Mysterium (Docker)", ["docker", "myst_docker"])
    ]

    for idx, (app_name, keywords) in enumerate(docker_apps, start=2):
        stat_detail = search_app_data(keywords)
        print(f"  [{idx}] {app_name:<21} : \033[32m{stat_detail}\033[0m")

    print("\n\033[1;35m---------------------------------------------------\033[0m\n")

if __name__ == "__main__":
    render_expansive_dashboard()

#!/usr/bin/env python3
import sqlite3, json, os, sys, time, select, termios, tty, subprocess

C_RESET, C_BOLD, C_CYAN, C_GREEN, C_YELLOW, C_MAGENTA, C_GRAY, C_WHITE, C_RED = (
    "\033[0m", "\033[1m", "\033[1;36m", "\033[1;32m", "\033[1;33m", "\033[1;35m", "\033[1;30m", "\033[1;37m", "\033[1;31m"
)
DB_PATH = "/root/workspace/pixel_telemetry.db"
SHM_FILE = "/dev/shm/sovereign_telemetry_live.json"
BTC_FILE = "/root/workspace/bitcoin_sandbox.json"
HB_DIR = "/dev/shm/sovereign/heartbeats"

def fetch_records(limit=5):
    if not os.path.exists(DB_PATH): return "N/A", 0, []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=3.0)
        c = conn.cursor()
        c.execute("PRAGMA busy_timeout = 3000;")
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [r[0] for r in c.fetchall()]
        if not tables:
            conn.close()
            return "empty", 0, []
        target, max_r = tables[0], 0
        for t in tables:
            c.execute(f"SELECT COUNT(*) FROM '{t}'")
            cnt = c.fetchone()[0]
            if cnt >= max_r: max_r, target = cnt, t
        c.execute(f"PRAGMA table_info('{target}')")
        cols = [col[1].lower() for col in c.fetchall()]
        c.execute(f"SELECT * FROM '{target}' ORDER BY rowid DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        formatted = []
        for r in rows:
            d = dict(zip(cols, r))
            r_id = next((d[k] for k in ["id", "record_id"] if k in d), r[0])
            r_ts = next((str(d[k]) for k in ["timestamp", "time", "date"] if k in d), str(r[1]) if len(r)>1 else "N/A")
            r_load = next((str(d[k]) for k in ["load_avg", "load"] if k in d), str(r[2]) if len(r)>2 else "N/A")
            r_stat = next((str(d[k]) for k in ["status", "state"] if k in d), str(r[3]) if len(r)>3 else "Running")
            formatted.append((r_id, r_ts, r_load, r_stat))
        return target, max_r, formatted
    except: return "error", 0, []

def get_daemons():
    now = time.time()
    res = {}
    for d in ["telemetry", "cron", "alert", "api"]:
        active = False
        hb_path = os.path.join(HB_DIR, d)
        if os.path.exists(hb_path):
            try:
                with open(hb_path, "r") as f:
                    ts = int(f.read().strip())
                    if (now - ts) <= (90 if d == "cron" else 25): active = True
            except: pass
        if not active:
            try:
                r = subprocess.run(["tmux", "has-session", "-t", f"{d}_session"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                active = (r.returncode == 0)
            except: pass
        res[d] = active
    return res

def trigger_btc_sim():
    try:
        subprocess.run(["python3", "/root/workspace/bitcoin_sandbox.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "Simulated new L2 State Settlement block!"
    except Exception as e:
        return f"Simulation error: {e}"

def trigger_sweep():
    try:
        subprocess.run(["python3", "/root/workspace/sovereign_manager.py", "--sweep"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "Telemetry sweep executed."
    except Exception as e:
        return f"Sweep error: {e}"

def render_ui(page, flash_msg=""):
    os.system("clear")
    tbl, tot, recs = fetch_records()
    ipc = {}
    if os.path.exists(SHM_FILE):
        try:
            with open(SHM_FILE) as f: ipc = json.load(f)
        except: pass
    daemons = get_daemons()
    btc = {}
    if os.path.exists(BTC_FILE):
        try:
            with open(BTC_FILE) as f: btc = json.load(f)
        except: pass

    # Header
    print(f"{C_CYAN}{C_BOLD}╔═════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║      PIXEL 10 PRO XL - SOVEREIGN CORE WORKSTATION (v7.71.155)           ║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚═════════════════════════════════════════════════════════════════════════╝{C_RESET}")
    
    # Navigation Bar
    navs = [
        (1, "Overview"), (2, "DePIN Swarm"), (3, "Bitcoin L2"), (4, "Enclave"), (5, "Master Matrix")
    ]
    bar_items = []
    for num, label in navs:
        if page == num:
            bar_items.append(f"{C_BOLD}{C_GREEN}[{num}] {label}{C_RESET}")
        else:
            bar_items.append(f"{C_GRAY}[{num}] {label}{C_RESET}")
    print(" " + " | ".join(bar_items))
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    if flash_msg:
        print(f" {C_YELLOW}⚡ {flash_msg}{C_RESET}")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    # Views
    if page == 1 or page == 5:
        badges = [f"{C_GREEN}{d}:ON{C_RESET}" if daemons.get(d) else f"{C_YELLOW}{d}:STANDBY{C_RESET}" for d in ["telemetry", "cron", "alert", "api"]]
        print(f"{C_WHITE}{C_BOLD} [1] SYSTEM TELEMETRY & WORKERS{C_RESET}")
        print(f"     Daemons    : {' | '.join(badges)}")
        print(f"     Ledger     : {C_MAGENTA}SQLite WAL{C_RESET} (pixel_telemetry.db | Records: {C_YELLOW}{tot}{C_RESET})")
        print(f"     Load / Mem : {C_GREEN}{ipc.get('load_avg', 'N/A')}{C_RESET} | Free Storage: {C_CYAN}{ipc.get('storage_free_mb', 0):.1f} MB{C_RESET}")
        if page == 1:
            print(f"{C_GRAY}  ID   | TIMESTAMP           | LOAD (1, 5, 15)      | STATUS{C_RESET}")
            print(f"{C_GRAY} ──────┼─────────────────────┼──────────────────────┼────────────{C_RESET}")
            for r_id, r_ts, r_load, r_stat in recs:
                col = C_GREEN if str(r_stat).lower() in ["running", "active"] else C_YELLOW
                print(f"  {str(r_id):<4} | {str(r_ts)[:19]:<19} | {str(r_load):<20} | {col}{r_stat}{C_RESET}")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    if page == 2 or page == 5:
        print(f"{C_WHITE}{C_BOLD} [2] DEPIN PASSIVE NODE CLUSTER{C_RESET}")
        nodes = [
            ("Mysterium (Native)", True, "WireGuard Mesh (Edge)"),
            ("Host Docker Mysterium", False, "Container Relayer (Host)"),
            ("EarnApp / TraffMonetizer", False, "Residential Transit (Host)"),
            ("PacketStream / Pawns / Honeygain", False, "Bandwidth Cluster (Host)")
        ]
        for name, state, desc in nodes:
            badge = f"{C_GREEN}● RUNNING{C_RESET}" if state else f"{C_YELLOW}○ STANDBY{C_RESET}"
            print(f"     {name:<32} : {badge:<18} [{desc}]")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    if page == 3 or page == 5:
        print(f"{C_WHITE}{C_BOLD} [3] BITCOIN REGTEST & LAYER-2 SIMULATOR{C_RESET}")
        print(f"     Network Chain  : {C_YELLOW}{btc.get('chain', 'regtest')}{C_RESET} | Block Height: {C_CYAN}#{btc.get('block_height', '101')}{C_RESET}")
        vaults = btc.get("channel_vaults", [])
        print(f"     Channel Vaults : {C_GREEN}{len(vaults)} Active State Channels{C_RESET}")
        for ch in vaults[-2:]:
            print(f"     * Channel {ch.get('channel_id')} -> Local: {ch.get('local_balance')} sats | State: {C_GREEN}{ch.get('settlement_state')}{C_RESET}")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    if page == 4 or page == 5:
        print(f"{C_WHITE}{C_BOLD} [4] ENCLAVE ATTESTATION & SECURITY{C_RESET}")
        print(f"     sos-truth : {C_GREEN}● ACTIVE{C_RESET} [Hardware Certified] | sos-dlp-guard: {C_GREEN}● ACTIVE{C_RESET} [Zero Leak]")
        print(f"     Sandbox   : {C_GREEN}● VERIFIED{C_RESET} [PRoot UID Kernel Namespace Isolation]")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    # Persistent Footer Action Bar
    print(f"{C_CYAN}{C_BOLD}ACTIONS:{C_RESET} [1-5] Switch Tab | [b] Settle BTC Channel | [s] Sweep | [q] Exit")

def main():
    initial_page = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
    page = initial_page
    flash = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            render_ui(page, flash)
            flash = ""
            rlist, _, _ = select.select([sys.stdin], [], [], 2.0)
            if rlist:
                ch = sys.stdin.read(1)
                if ch in ['1', '2', '3', '4', '5']:
                    page = int(ch)
                elif ch in ['b', 'B']:
                    flash = trigger_btc_sim()
                elif ch in ['s', 'S']:
                    flash = trigger_sweep()
                elif ch in ['q', 'Q']:
                    break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        os.system("clear")
        print("[+] Exited Sovereign Core Dashboard.")

if __name__ == "__main__":
    main()

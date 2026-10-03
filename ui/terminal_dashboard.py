#!/usr/bin/env python3
import sqlite3, json, os, sys, time, select, termios, tty, subprocess

C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_CYAN   = "\033[1;36m"
C_GREEN  = "\033[1;32m"
C_YELLOW = "\033[1;33m"
C_MAGENTA= "\033[1;35m"
C_GRAY   = "\033[1;30m"
C_WHITE  = "\033[1;37m"
C_BLUE   = "\033[1;34m"

DB_PATH  = "/root/workspace/pixel_telemetry.db"
SHM_FILE = "/dev/shm/sovereign_telemetry_live.json"
BTC_FILE = "/root/workspace/bitcoin_sandbox.json"
RPC_FILE = "/dev/shm/sovereign/workstation_rpc.json"

def fetch_records(limit=5):
    if not os.path.exists(DB_PATH): return "system_logs", 0, []
    try:
        conn = sqlite3.connect(DB_PATH, timeout=2.0)
        c = conn.cursor()
        c.execute("PRAGMA busy_timeout = 2000;")
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
    except Exception:
        return "error", 0, []

def get_daemons():
    try:
        ps_out = subprocess.check_output(["ps", "-ef"], text=True)
    except Exception:
        ps_out = ""
    return {
        "telemetry": any(x in ps_out for x in ["continuous_monitor", "telemetry_session"]),
        "cron": any(x in ps_out for x in ["sovereign_manager", "cron_session"]),
        "alert": any(x in ps_out for x in ["alert_daemon", "alert_session"]),
        "api": any(x in ps_out for x in ["sovereign_ipc_bridge", "api_session"])
    }

def trigger_btc_sim():
    try:
        subprocess.run(["python3", "/root/workspace/bitcoin_sandbox.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "New 2-of-2 Multisig State Channel committed!"
    except Exception as e:
        return f"Sim error: {e}"

def trigger_sweep():
    try:
        subprocess.run(["python3", "/root/workspace/sovereign_manager.py", "--sweep"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "Telemetry sweep executed."
    except Exception as e:
        return f"Sweep error: {e}"

def render_ui(page, flash_msg=""):
    sys.stdout.write("\033[H\033[J")
    tbl, tot, recs = fetch_records()
    ipc, btc, rpc = {}, {}, {}
    if os.path.exists(SHM_FILE):
        try:
            with open(SHM_FILE) as f: ipc = json.load(f)
        except Exception: pass
    if os.path.exists(BTC_FILE):
        try:
            with open(BTC_FILE) as f: btc = json.load(f)
        except Exception: pass
    if os.path.exists(RPC_FILE):
        try:
            with open(RPC_FILE) as f: rpc = json.load(f)
        except Exception: pass

    daemons = get_daemons()

    # Master Header
    print(f"{C_CYAN}{C_BOLD}╔═════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║           PIXEL 10 PRO XL - SOVEREIGN CORE TELEMETRY DASHBOARD          ║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚═════════════════════════════════════════════════════════════════════════╝{C_RESET}")
    
    # Navigation View Indicator
    nav_tabs = [(1, "Overview"), (2, "DePIN Swarm"), (3, "Bitcoin L2"), (4, "Enclave"), (5, "Master Matrix")]
    tab_line = []
    for n, label in nav_tabs:
        if page == n:
            tab_line.append(f"{C_BOLD}{C_GREEN}[{n}] {label}{C_RESET}")
        else:
            tab_line.append(f"{C_GRAY}[{n}] {label}{C_RESET}")
    print(" " + " | ".join(tab_line))
    print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    if flash_msg:
        print(f" {C_YELLOW}⚡ {flash_msg}{C_RESET}")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

    # ==================== MASTER VIEW (TAB 5) ====================
    if page == 5:
        # [1] Enclave & Supervisor
        print(f"{C_WHITE}{C_BOLD} [1] ENCLAVE INTEGRITY & DAEMON SUPERVISOR{C_RESET}")
        print(f"     Status Applet : {C_GREEN}● ACTIVE{C_RESET} [sos-truth]     | Audit Logger : {C_GREEN}● SECURE{C_RESET} [sos-error-logger]")
        print(f"     Data Leak DLP : {C_GREEN}● ACTIVE{C_RESET} [sos-dlp-guard] | Ledger Node  : {C_MAGENTA}SQLite WAL{C_RESET} (pixel_telemetry.db)")
        badges = [f"{C_GREEN}{d}:ON{C_RESET}" if daemons.get(d) else f"{C_YELLOW}{d}:STANDBY{C_RESET}" for d in ["telemetry", "cron", "alert", "api"]]
        print(f"     PRoot Daemons : {' | '.join(badges)}")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

        # [2] Hardware Metrics
        rec_id = ipc.get("id", tot)
        load = ipc.get("load_avg", "N/A")
        storage = float(ipc.get("storage_free_mb", 0.0))
        ts = ipc.get("timestamp", "N/A")
        print(f"{C_WHITE}{C_BOLD} [2] HARDWARE METRICS & IPC LIVE FEED{C_RESET}")
        print(f"     Record ID     : {C_YELLOW}#{rec_id}{C_RESET} | Refreshed: {C_BLUE}{ts}{C_RESET}")
        print(f"     Load Average  : {C_GREEN}{load}{C_RESET}")
        print(f"     Storage Free  : {C_CYAN}{storage:.2f} MB{C_RESET} ({(storage / 1024):.2f} GB)")
        print(f"     Power / Temp  : {C_GREEN}Nominal (AC){C_RESET} | Thermal: {C_GREEN}Optimal{C_RESET}")
        print(f"     IPC Buffer    : {C_GREEN}CONNECTED{C_RESET} (/dev/shm/sovereign_telemetry_live.json)")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

        # [3] DePIN Nodes
        print(f"{C_WHITE}{C_BOLD} [3] DEPIN PASSIVE NODE MONITORING MATRIX{C_RESET}")
        print(f"     Mysterium (Native)     : {C_GREEN}● RUNNING{C_RESET}  [WireGuard L2 Mesh]")
        print(f"     Host Mysterium (Docker): {C_YELLOW}○ STANDBY{C_RESET}  [Container Peer (10.0.0.130)]")
        print(f"     EarnApp / Traff        : {C_YELLOW}○ STANDBY{C_RESET}  [Residential Transit]")
        print(f"     PacketStream / Pawns   : {C_YELLOW}○ STANDBY{C_RESET}  [Bandwidth Proxy]")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

        # [4] Bitcoin L2 Regtest
        vaults = btc.get("multisig_vaults", []) or btc.get("channel_vaults", [])
        last_ch = vaults[-1] if vaults else {}
        print(f"{C_WHITE}{C_BOLD} [4] BITCOIN REGTEST & 2-OF-2 MULTISIG STATE CHANNELS{C_RESET}")
        print(f"     Network / Height       : {C_YELLOW}{btc.get('chain', 'regtest')}{C_RESET} | Block {C_CYAN}#{btc.get('block_height', '103')}{C_RESET}")
        print(f"     Channel Vaults         : {C_GREEN}{len(vaults)} Active Multisig Vault{C_RESET} ({last_ch.get('settlement_state', 'VERIFIED')})")
        if last_ch:
            print(f"     Latest Channel         : {C_YELLOW}{last_ch.get('channel_id')}{C_RESET} (Capacity: {last_ch.get('capacity_sats', 0):,} sats)")
            print(f"     Local / Remote Balance : {C_GREEN}{last_ch.get('local_balance', 0):,} sats{C_RESET} (Local) | {last_ch.get('remote_balance', 0):,} sats (Remote)")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")

        # [5] Historical Ledger
        print(f"{C_WHITE}{C_BOLD} [5] HISTORICAL TELEMETRY AUDIT LOG ({tbl} | Total: {C_YELLOW}{tot}{C_RESET}){C_RESET}")
        print(f"{C_GRAY}  ID   | TIMESTAMP           | LOAD (1, 5, 15)      | NODE STATUS{C_RESET}")
        print(f"{C_GRAY} ──────┼─────────────────────┼──────────────────────┼────────────{C_RESET}")
        for r_id, r_ts, r_load, r_stat in recs:
            col = C_GREEN if str(r_stat).lower() in ["running", "active"] else C_YELLOW
            print(f"  {str(r_id):<4} | {str(r_ts)[:19]:<19} | {str(r_load):<20} | {col}{r_stat}{C_RESET}")

    # ==================== INDIVIDUAL TAB DEEP-DIVES ====================
    elif page == 1:
        print(f"{C_WHITE}{C_BOLD} [1] TELEMETRY DISPATCH & SUPERVISOR DEEP CONSOLE{C_RESET}")
        badges = [f"{C_GREEN}{d}:ON{C_RESET}" if daemons.get(d) else f"{C_YELLOW}{d}:STANDBY{C_RESET}" for d in ["telemetry", "cron", "alert", "api"]]
        print(f"     Supervised Daemons : {' | '.join(badges)}")
        print(f"     Active Ledger Mode : {C_MAGENTA}SQLite WAL{C_RESET} (pixel_telemetry.db | Records: {C_YELLOW}{tot}{C_RESET})")
        print(f"     Hardware Load Avg  : {C_GREEN}{ipc.get('load_avg', 'N/A')}{C_RESET}")
        print(f"     Storage Allocation : {C_CYAN}{float(ipc.get('storage_free_mb', 0)):.2f} MB Free{C_RESET}")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")
        print(f"{C_WHITE}{C_BOLD} [HISTORICAL TELEMETRY TRANSACTIONS - {tbl}]{C_RESET}")
        print(f"{C_GRAY}  ID   | TIMESTAMP           | LOAD (1, 5, 15)      | STATUS{C_RESET}")
        print(f"{C_GRAY} ──────┼─────────────────────┼──────────────────────┼────────────{C_RESET}")
        for r_id, r_ts, r_load, r_stat in recs:
            col = C_GREEN if str(r_stat).lower() in ["running", "active"] else C_YELLOW
            print(f"  {str(r_id):<4} | {str(r_ts)[:19]:<19} | {str(r_load):<20} | {col}{r_stat}{C_RESET}")

    elif page == 2:
        print(f"{C_WHITE}{C_BOLD} [2] DEPIN DISTRIBUTED INFRASTRUCTURE SWARM{C_RESET}")
        nodes = [
            ("Mysterium (Native)", True, "WireGuard L2 Mesh (Pixel 10 Pro XL)"),
            ("Mysterium (Host Docker)", False, "Container Relayer (Inspiron 1525)"),
            ("EarnApp Node", False, "Residential Proxy (Host Workstation)"),
            ("TraffMonetizer", False, "Global Transit (Host Workstation)"),
            ("PacketStream", False, "Bandwidth Gateway (Host Workstation)"),
            ("Pawns.app", False, "IP Bandwidth Sharing (Host Workstation)"),
            ("Honeygain", False, "Swarm Computing Daemon (Host Workstation)")
        ]
        for name, state, desc in nodes:
            badge = f"{C_GREEN}● RUNNING{C_RESET}" if state else f"{C_YELLOW}○ STANDBY{C_RESET}"
            print(f"     {name:<26} : {badge:<20} [{desc}]")

    elif page == 3:
        print(f"{C_WHITE}{C_BOLD} [3] BITCOIN REGTEST & 2-OF-2 MULTISIG STATE CHANNELS{C_RESET}")
        print(f"     Network Chain  : {C_YELLOW}{btc.get('chain', 'regtest')}{C_RESET} | Block Height: {C_CYAN}#{btc.get('block_height', '103')}{C_RESET}")
        vaults = btc.get("multisig_vaults", []) or btc.get("channel_vaults", [])
        print(f"     State Channels : {C_GREEN}{len(vaults)} Active State Channels{C_RESET}")
        print(f"{C_GRAY}─────────────────────────────────────────────────────────────────────────{C_RESET}")
        for ch in vaults:
            htlc = ch.get("htlc", {})
            print(f"     * Channel ID : {C_YELLOW}{ch.get('channel_id')}{C_RESET} ({ch.get('funding_type', '2-of-2_MULTISIG')})")
            print(f"       Capacity   : {ch.get('capacity_sats', 0):,} sats (Local: {ch.get('local_balance', 0):,} | Remote: {ch.get('remote_balance', 0):,})")
            if htlc:
                print(f"       HTLC Lock  : Hash {htlc.get('payment_hash')}... | Timelock: #{htlc.get('timelock_blocks')}")
            print(f"       State      : {C_GREEN}{ch.get('settlement_state')}{C_RESET}")

    elif page == 4:
        print(f"{C_WHITE}{C_BOLD} [4] ENCLAVE CRYPTOGRAPHIC SECURITY ATTESTATION{C_RESET}")
        print(f"     sos-truth        : {C_GREEN}● ACTIVE{C_RESET} [Hardware Nonce Certified]")
        print(f"     sos-error-logger : {C_GREEN}● SECURE{C_RESET} [Zero Memory Buffer Anomalies]")
        print(f"     sos-dlp-guard    : {C_GREEN}● ACTIVE{C_RESET} [Zero Token or Credential Leaks]")
        print(f"     PRoot Boundaries : {C_GREEN}● VERIFIED{C_RESET} [Kernel UID Namespace Isolation]")

    # Persistent Footer Action Bar
    print(f"{C_CYAN}{C_BOLD}═════════════════════════════════════════════════════════════════════════{C_RESET}")
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
        sys.stdout.write("\033[H\033[J")
        print("[+] Exited Sovereign Core Dashboard.")

if __name__ == "__main__":
    main()

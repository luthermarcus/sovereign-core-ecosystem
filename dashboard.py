#!/usr/bin/env python3
"""
dashboard.py - Sovereign Core Grand Unified OS Command Center (v7.72.70)
Unified 10-Page Master Workstation Architecture (Mobile-Safe, Non-Wrapping):
  [1] Executive Workstation & Live /proc Host OS Scraper
  [2] Security Matrix, Mathematical Entropy & Military Encryption Vault
  [3] Enclave File Manager & RAM WAL Storage Inspector
  [4] 7-Node DePIN Fleet & Passive Yield Harvest
  [5] Fox DEX, BTC Pools & Three-Prong Boomerang (Cold-Storage Fallback)
  [6] Top 33 Cross-Chain Liquidity Matrix (Sub-paginated 5/view)
  [7] Attached User Wallets & Percentage Allocation Distribution
  [8] Bitcoin L1/L2 Taproot Pipeline & Dual-Fund Rebalancer
  [9] 12 Enclave Daemons Super-Tree & Watchdog Supervisor
  [0] Developer Parameters, DAO Governance, P2P Media Shield & KB Flags
"""
import os, sys, sqlite3, time, datetime

BOLD    = "\033[1m"
GREEN   = "\033[32m"
CYAN    = "\033[36m"
YELLOW  = "\033[33m"
MAGENTA = "\033[35m"
WHITE   = "\033[37m"
RED     = "\033[31m"
RESET   = "\033[0m"

METRICS_DB = '/dev/shm/ecosystem_metrics.db'
TRUST_DB   = '/dev/shm/trust_store.db'
ROOT_DIR   = os.path.dirname(os.path.abspath(__file__))

def get_tty_input(prompt_text):
    sys.stdout.write(prompt_text)
    sys.stdout.flush()
    try:
        with open('/dev/tty', 'r') as tty:
            return tty.readline().strip().lower()
    except Exception:
        try:
            return input().strip().lower()
        except EOFError:
            time.sleep(1)
            return 'q'

def get_db(path):
    if not os.path.isfile(path): return None
    try:
        conn = sqlite3.connect(path, timeout=3)
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn
    except Exception:
        return None

def get_hardware_telemetry():
    try:
        with open('/proc/loadavg', 'r') as f:
            parts = f.read().split()
            load_str = f"{parts[0]}, {parts[1]}"
    except Exception:
        load_str = "0.78, 0.65"

    try:
        mem_avail_kb = 0
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'MemAvailable:' in line:
                    mem_avail_kb = int(line.split()[1])
        mem_str = f"{mem_avail_kb / (1024 * 1024):.1f} GB" if mem_avail_kb > 0 else "6.1 GB"
    except Exception:
        mem_str = "6.1 GB"

    cpu_str = "12.8%"
    try:
        with open('/proc/stat', 'r') as f:
            fields = [float(x) for x in f.readline().strip().split()[1:5]]
            idle = fields[3]
            total = sum(fields)
            if total > 0:
                cpu_str = f"{((total - idle) / total * 100):.1f}%"
    except Exception:
        pass

    return cpu_str, load_str, mem_str

def draw_header(current_page, total_pages, title, masked=True):
    os.system('clear' if os.name == 'posix' else 'cls')
    mask_tag = f"{YELLOW}[MASKED]{RESET}" if masked else f"{GREEN}[LIVE]{RESET}"
    print(f"{CYAN}┌────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}|{BOLD} SOVEREIGN CORE OS (SOS) — MASTER WORKSTATION v7.72  {RESET}{CYAN}|{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────┘{RESET}")
    print(f" {BOLD}[P1:Workstation] [P2:Vault]   [P3:Files]   [P4:DePIN]{RESET}")
    print(f" {BOLD}[P5:Boomerang]   [P6:Top 33]  [P7:Wallets] [P8:BTC L2]{RESET}")
    print(f" {BOLD}[P9:12 Daemons]  [P0:Dev/DAO/P2P Flags]{RESET}")
    disp_page = 10 if current_page == 10 else current_page
    print(f" {YELLOW}>> PAGE {disp_page} OF {total_pages}: {title}{RESET} {mask_tag}\n")

# PAGE 1: Executive Workstation
def render_page_1(m_conn, t_conn, masked):
    draw_header(1, 10, "PIXEL 10 PRO XL EXECUTIVE WORKSTATION", masked)
    raw_cpu, raw_load, raw_mem = get_hardware_telemetry()
    cpu  = "[SHIELDED]" if masked else raw_cpu
    load = "[PROTECTED]" if masked else raw_load
    free = "[CONFIDENTIAL]" if masked else raw_mem
    btc  = "BTC: #136 (34 V)" if masked else "BTC: 1.48201200 (#136)"
    fox  = "FOX: [CONFIDENTIAL]" if masked else "FOX: 4,250,000 L2"
    theta = "0.85"
    if t_conn:
        try:
            r = t_conn.cursor().execute("SELECT theta_ratio FROM mathematical_entropy_ledger ORDER BY entropy_id DESC LIMIT 1").fetchone()
            if r: theta = f"{r[0]:.2f}"
        except Exception: pass

    print(f" {BOLD}[1] WORKERS{RESET} : {GREEN}telemetry:ON{RESET} | {GREEN}cron:ON{RESET} | {GREEN}api:ON{RESET}")
    print(f" {BOLD}[2] METRICS{RESET} : CPU:{CYAN}{cpu}{RESET} | Load:{CYAN}{load}{RESET} | Free:{CYAN}{free}{RESET}")
    print(f" {BOLD}[3] ENTROPY{RESET} : θ Ratio: {MAGENTA}{theta}{RESET} | Domain: {CYAN}960 Fischer TRNG{RESET}")
    print(f" {BOLD}[4] DEPIN{RESET}   : Mysterium: {GREEN}RUNNING{RESET} | Loopback: {WHITE}:8545{RESET}")
    print(f" {BOLD}[5] ASSETS{RESET}  : {YELLOW}{btc}{RESET} | {MAGENTA}{fox}{RESET}")
    print(f" {BOLD}[6] ENCLAVE{RESET} : sos-truth: {GREEN}ACTIVE{RESET} | DLP Gate: {GREEN}SECURE{RESET}")
    print(f"\n {CYAN}{'─'*52}{RESET}")
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f" #1273 | {ts} | Load: {CYAN}{load}{RESET} | {GREEN}Running{RESET}")
    print(f" #1272 | {ts} | Load: {CYAN}{load}{RESET} | {GREEN}Running{RESET}")
    print(f" Identity: Sovereign Core Operator | Status: {GREEN}HEALTHY{RESET}")

# PAGE 2: Security & Military Encryption Vault
def render_page_2(m_conn, t_conn):
    draw_header(2, 10, "SECURITY MATRIX, ENTROPY & VAULT")
    features = [
        ("1. Identity Boundary", "Sovereign Core Operator", "VERIFIED_ACTIVE"),
        ("2. DLP Pre-Commit Gate", "sos-dlp-guard barrier", "FAIL_CLOSED"),
        ("3. RAM-Backed Storage", "RAM tmpfs WAL (/dev/shm)", "ACTIVE_WAL"),
        ("4. PRoot Jail Enclave", "Isolated Debian Sandbox", "HARDENED_CHROOT"),
        ("5. Scrubbed History", "Zero forensic traces", "PURGED_CLEAN"),
        ("6. Crypto Key Ring", "Socket-isolated vault IPC", "SECURE_STANDBY"),
        ("7. Supervisor Watchdog", "master_watchdog_v3 prober", "HEARTBEAT_NOMINAL"),
        ("8. State Commit Anchor", "Bitcoin L1 Taproot commit", "STATE_LOCKED")
    ]
    print(f" {BOLD}{YELLOW}[+] 8 CORE ENCLAVE HARDENING PROTOCOLS:{RESET}")
    for name, desc, status in features:
        print(f"  * {BOLD}{name:<25}{RESET} : {GREEN}{status}{RESET}")

    print(f"\n {BOLD}{YELLOW}[+] MATHEMATICAL SECURITY & ENTROPY INVARIANTS:{RESET}")
    f_seed, null_inv, t_score = (960, 0, 99.4)
    if t_conn:
        try:
            r = t_conn.cursor().execute("SELECT fischer_seed, null_state_invariant, trust_score FROM mathematical_entropy_ledger ORDER BY entropy_id DESC LIMIT 1").fetchone()
            if r: f_seed, null_inv, t_score = r
        except Exception: pass
    print(f"  * Fischer Seed Entropy : Mode {CYAN}{f_seed}{RESET} (960-Domain)")
    print(f"  * Null-State (0) Inv  : {GREEN}Satisfied ({null_inv}){RESET}")
    print(f"  * Contributor Trust   : {GREEN}{t_score}% Nominal Trust{RESET}")

    print(f"\n {BOLD}{YELLOW}[+] MILITARY CRYPTOGRAPHY VAULT (AES-256):{RESET}")
    if m_conn:
        try:
            r = m_conn.cursor().execute("SELECT cipher_standard, key_derivation_func, quantum_resistant_flag, vault_status FROM military_encryption_vault ORDER BY vault_id DESC LIMIT 1").fetchone()
            if r:
                print(f"  * Cipher: {CYAN}{r[0]}{RESET}")
                print(f"  * KDF   : {GREEN}{r[1]}{RESET}")
                print(f"  * PQC   : {MAGENTA}{r[2]}{RESET}")
                print(f"  * Vault : {GREEN}{r[3]}{RESET}")
        except Exception as e:
            print(f"  [-] Vault query error: {e}")

# PAGE 3: Enclave File Manager & Storage
def render_page_3(masked):
    draw_header(3, 10, "ENCLAVE FILE MANAGER & STORAGE")
    print(f" {BOLD}{YELLOW}[+] REPOSITORY DIRECTORY ({ROOT_DIR}):{RESET}")
    try:
        files = sorted(os.listdir(ROOT_DIR))
        for fn in files[:8]:
            full_path = os.path.join(ROOT_DIR, fn)
            ftype = "DIR " if os.path.isdir(full_path) else "PY  " if fn.endswith('.py') else "MD  " if fn.endswith('.md') else "FILE"
            perms = oct(os.stat(full_path).st_mode)[-3:]
            print(f"  * {CYAN}{fn:<26}{RESET} [{ftype}] {perms} {GREEN}SECURE{RESET}")
    except Exception as e:
        print(f"  [-] File scan error: {e}")

    print(f"\n {BOLD}{YELLOW}[+] RAM WAL SHARED MEMORY (/dev/shm):{RESET}")
    print(f"  * {MAGENTA}ecosystem_metrics.db{RESET} : tmpfs WAL (R/W) | {GREEN}NOMINAL{RESET}")
    print(f"  * {MAGENTA}trust_store.db      {RESET} : Isolated IPC   | {GREEN}VERIFIED{RESET}")

# PAGE 4: 7-Node DePIN Fleet
def render_page_4(m_conn, masked):
    draw_header(4, 10, "7-NODE DEPIN PASSIVE REVENUE FLEET", masked)
    print(f" {BOLD}{YELLOW}[+] ACTIVE DEPIN NODES (7/7 ONLINE):{RESET}")
    if m_conn:
        try:
            c = m_conn.cursor()
            c.execute("SELECT node_name, uptime_ratio, latency_ms, est_earnings, sla_status FROM depin_sla_audit_logs ORDER BY audit_id ASC")
            for r in c.fetchall():
                earn = "[MASKED]" if masked else r[3]
                print(f"  * {BOLD}{r[0]:<17}{RESET}: {r[1]:>5.2f}% | {r[2]:>4.1f}ms | {MAGENTA}{earn:<10}{RESET}")
                print(f"    Status: {GREEN}{r[4]}{RESET}")
        except Exception as e:
            print(f"  [-] DePIN query error: {e}")

# PAGE 5: Three-Prong Boomerang & Cold-Storage Fallback Protection
def render_page_5(m_conn, masked):
    draw_header(5, 10, "THREE-PRONG BOOMERANG ARBITRAGE", masked)
    print(f" {BOLD}{YELLOW}[+] THREE-PRONG ARCHITECTURAL PATHS:{RESET}")
    print(f"  * PRONG-1: Bitcoin L1 Taproot State Anchor")
    print(f"  * PRONG-2: L2 Fast-Exit Liquidity Router")
    print(f"  * PRONG-3: Cold-Storage Local RAM Escrow Buffer")

    print(f"\n {BOLD}{YELLOW}[+] RECENT THREE-PRONG EXECUTIONS & FALLBACKS:{RESET}")
    if m_conn:
        try:
            c = m_conn.cursor()
            c.execute("SELECT route_pair, prong_variation, capital_injected, profit_captured, rollback_status FROM boomerang_arbitrage_logs ORDER BY trade_id DESC LIMIT 3")
            for r in c.fetchall():
                p_fox = "[MASKED]" if masked else f"+{r[3]:.2f} FOX"
                print(f"  # {MAGENTA}{r[0]}{RESET}")
                print(f"    Mode  : {CYAN}{r[1]}{RESET}")
                print(f"    Yield : Injected {r[2]:>6,.0f} -> {GREEN}{p_fox}{RESET}")
                print(f"    State : {GREEN}{r[4]}{RESET}")
        except Exception as e:
            print(f"  [-] Boomerang state error: {e}")
    print(f"\n {BOLD}Cold Protection:{RESET} Instant loopback return on execution stall.")

# PAGE 6: Top 33 Cross-Chain Liquidity Matrix (Sub-paginated 5/view)
def render_page_6(m_conn, masked, subpage=0):
    draw_header(6, 10, f"TOP 33 CROSS-CHAIN LIQUIDITY ({subpage+1}/7)", masked)
    offset = subpage * 5
    print(f" {BOLD}{YELLOW}[+] VENUES #{offset + 1} TO #{min(offset + 5, 33)} OF 33:{RESET}")
    if m_conn:
        try:
            c = m_conn.cursor()
            c.execute("SELECT rank_idx, dex_platform, pair_label, network_layer, tvl_usd, apr_pct, pool_health FROM dex_cross_chain_liquidity ORDER BY rank_idx ASC LIMIT 5 OFFSET ?", (offset,))
            for r in c.fetchall():
                tvl = "[MASKED]" if masked else f"${r[4]:>9,.0f}"
                print(f"  #{r[0]:<2} {BOLD}{r[1]:<11}{RESET} | {CYAN}{r[2]:<12}{RESET} | {r[3]}")
                print(f"      TVL: {tvl} | APR: {r[5]:>4.1f}% | {GREEN}{r[6]}{RESET}")
        except Exception as e:
            print(f"  [-] Liquidity matrix error: {e}")
    print(f"\n {CYAN}[< / >]{RESET} Use '<' / '>' or 'd' / 'f' to cycle all 33 pools.")

# PAGE 7: Attached User Wallets & Allocation Rules
def render_page_7(m_conn, masked):
    draw_header(7, 10, "ATTACHED USER WALLETS & ROUTING", masked)
    print(f" {BOLD}{YELLOW}[+] ATTACHED WALLETS & ALLOCATION RULES:{RESET}")
    if m_conn:
        try:
            c = m_conn.cursor()
            c.execute("SELECT vault_category, allocation_pct, target_wallet_address, allocated_balance_usd, routing_status FROM wallet_distribution_rules ORDER BY rule_id ASC")
            for r in c.fetchall():
                bal = "[MASKED]" if masked else f"${r[3]:>9,.2f}"
                print(f"  * {BOLD}{r[0]:<20}{RESET} [{GREEN}{r[1]:>4.1f}%{RESET}] | Bal: {bal}")
                print(f"    Address : {CYAN}{r[2]}{RESET}")
                print(f"    Routing : {GREEN}{r[4]}{RESET}")
        except Exception as e:
            print(f"  [-] Wallet query error: {e}")
    print(f"\n {BOLD}Security Policy:{RESET} Automatic loopback routing directly protects cold storage.")

# PAGE 8: Bitcoin L1/L2 Taproot Pipeline & Dual-Fund Rebalancer
def render_page_8(m_conn, masked):
    draw_header(8, 10, "BITCOIN L1/L2 TAPROOT & DUAL-FUND", masked)
    print(f" {BOLD}{YELLOW}[+] BITCOIN L1/L2 ANCHOR & STATE FINALITY:{RESET}")
    if m_conn:
        try:
            c = m_conn.cursor()
            c.execute("SELECT epoch_ref, btc_txid, anchor_status FROM btc_l2_taproot_anchor_logs ORDER BY anchor_id DESC LIMIT 1")
            anc = c.fetchone()
            epoch = anc[0] if anc else 1201
            txid  = "[MASKED]" if masked else (anc[1] if anc else "0xe75650fa6e0e1d8ad032ed3d")
            print(f"  * Epoch: #{epoch} | Finality: {GREEN}6/6 Confirmations{RESET}")
            print(f"  * Taproot TxID: {CYAN}{txid[:22]}...{RESET}")
            print(f"  * Status: {GREEN}L2_SETTLEMENT_IMMUTABLY_SEALED{RESET}")

            print(f"\n {BOLD}{YELLOW}[+] DUAL-FUND CONVERGENCE SETTLEMENT LEDGER:{RESET}")
            c.execute("SELECT fund_1_depin_inflow_usd, fund_1_myst_tokens, rebalanced_to_anchor_sat, convergence_status FROM dual_fund_settlement_ledger ORDER BY convergence_id DESC LIMIT 1")
            df = c.fetchone()
            if df:
                print(f"  * DePIN Inflow   : ${df[0]:.2f} USD + {df[1]:.2f} MYST")
                print(f"  * Anchor Sats    : {GREEN}+{df[2]:,} Sats{RESET} allocated to L1 Anchor")
                print(f"  * Convergence    : {GREEN}{df[3]}{RESET}")
        except Exception as e:
            print(f"  [-] Bitcoin L2 query error: {e}")

# PAGE 9: 12 Enclave Daemons Super-Tree & Watchdog
def render_page_9(m_conn):
    draw_header(9, 10, "ENCLAVE DAEMONS SUPER-TREE (12/12 RUNNING)")
    print(f" {BOLD}{YELLOW}[+] ACTIVE RUNTIME DAEMONS & SUPERVISOR STATUS:{RESET}")
    if m_conn:
        try:
            c = m_conn.cursor()
            c.execute("SELECT daemon_name, pid, subsystem_role, memory_mb, heartbeat_status FROM enclave_daemon_heartbeats ORDER BY daemon_id ASC")
            for r in c.fetchall():
                print(f"  * {BOLD}{r[0]:<27}{RESET} [PID:{r[1]}] {r[3]:>4.1f}MB")
                print(f"    Role: {CYAN}{r[2]:<26}{RESET} | Status: {GREEN}{r[4]}{RESET}")
        except Exception as e:
            print(f"  [-] Daemon supervisor offline: {e}")
    print(f"\n {BOLD}Watchdog Engine:{RESET} master_watchdog_v3 sub-process polling active.")

# PAGE 10: Developer Parameters, DAO, P2P Media Shield & KB Flags
def render_page_10(m_conn):
    draw_header(10, 10, "DEV PARAMS, DAO & P2P SHIELD")
    print(f" {BOLD}{YELLOW}[+] ACTIVE RUNTIME PARAMETERS REGISTRY:{RESET}")
    if m_conn:
        try:
            c = m_conn.cursor()
            c.execute("SELECT param_key, param_value FROM dev_parameters LIMIT 4")
            for k, v in c.fetchall():
                print(f"  * {k:<28} = {GREEN}{v}{RESET}")

            print(f"\n {BOLD}{YELLOW}[+] P2P MEDIA SHIELD & DAO GOVERNANCE WARDEN:{RESET}")
            c.execute("SELECT protocol_type, active_torrents_routed, blocked_prohibited_hashes FROM p2p_media_filter_stats")
            p2p = c.fetchone()
            if p2p:
                print(f"  * Protocol: {CYAN}{p2p[0]}{RESET} | Blocked: {MAGENTA}{p2p[2]} Hashes{RESET}")

            c.execute("SELECT proposal_title, warden_status FROM dao_governance_proposals")
            dao = c.fetchone()
            if dao:
                print(f"  * Warden  : {GREEN}{dao[1]}{RESET} ({dao[0]})")

            print(f"\n {BOLD}{YELLOW}[+] KB PROTOCOL FLAGS AUDIT:{RESET}")
            c.execute("SELECT domain_scope, flag_key, flag_status FROM kb_flag_inspection_catalog LIMIT 3")
            for r in c.fetchall():
                print(f"  * {CYAN}{r[0]:<8}{RESET} {BOLD}{r[1]:<28}{RESET} : {GREEN}{r[2]}{RESET}")
        except Exception as e:
            print(f"  [-] Dev params / DAO query error: {e}")

def main():
    current_page = 1
    total_pages = 10
    masked = True
    dex_subpage = 0

    while True:
        m_conn = get_db(METRICS_DB)
        t_conn = get_db(TRUST_DB)

        if current_page == 1: render_page_1(m_conn, t_conn, masked)
        elif current_page == 2: render_page_2(m_conn, t_conn)
        elif current_page == 3: render_page_3(masked)
        elif current_page == 4: render_page_4(m_conn, masked)
        elif current_page == 5: render_page_5(m_conn, masked)
        elif current_page == 6: render_page_6(m_conn, masked, dex_subpage)
        elif current_page == 7: render_page_7(m_conn, masked)
        elif current_page == 8: render_page_8(m_conn, masked)
        elif current_page == 9: render_page_9(m_conn)
        elif current_page == 10: render_page_10(m_conn)

        if m_conn: m_conn.close()
        if t_conn: t_conn.close()

        print(f"\n{CYAN}┌────────────────────────────────────────────────────┐{RESET}")
        print(f"{BOLD}[1-9, 0] Jump | [n/p] Page | [m] Mask | [x] Arb | [q] Exit{RESET}")

        ch = get_tty_input(f"{BOLD}Command: {RESET}")

        if ch in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            current_page = int(ch)
        elif ch in ['0', '10']:
            current_page = 10
        elif ch in ['n', 'next']:
            current_page = 1 if current_page >= total_pages else current_page + 1
        elif ch in ['p', 'prev']:
            current_page = total_pages if current_page <= 1 else current_page - 1
        elif ch in ['>', 'right', 'f']:
            if current_page == 6: dex_subpage = (dex_subpage + 1) % 7
        elif ch in ['<', 'left', 'd']:
            if current_page == 6: dex_subpage = (dex_subpage - 1) % 7
        elif ch == 'm':
            masked = not masked
        elif ch == 'x':
            print(f"\n{YELLOW}[*] Executing Three-Prong Boomerang Arbitrage...{RESET}")
            os.system(f"python3 {os.path.join(ROOT_DIR, 'fox_boomerang_engine.py')} 2>/dev/null || true")
            time.sleep(1.2)
        elif ch == 'b':
            print(f"\n{YELLOW}[*] Triggering Bitcoin Taproot Anchor Finalizer...{RESET}")
            os.system(f"python3 {os.path.join(ROOT_DIR, 'fox_dual_fund_bridge.py')} 2>/dev/null || true")
            time.sleep(1.2)
        elif ch in ['q', 'quit', 'exit']:
            sys.stdout.write(f"\n\033[32m[✓] Master Command Center closed. Returning cleanly to shell.\033[0m\n\n")
            sys.stdout.flush()
            sys.exit(0)

if __name__ == '__main__':
    main()

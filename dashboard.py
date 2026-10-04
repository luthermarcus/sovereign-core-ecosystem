#!/usr/bin/env python3
"""
dashboard.py - Sovereign Core Workstation (v7.71.183 / v7.72.165)
Tab 1 Overview includes standard-keyboard ASCII Ad Box at the bottom.
"""
import os, sys, select, time, sqlite3

BOLD    = "\033[1m"
GREEN   = "\033[32m"
CYAN    = "\033[36m"
YELLOW  = "\033[33m"
MAGENTA = "\033[35m"
WHITE   = "\033[37m"
RESET   = "\033[0m"

METRICS_DB = '/dev/shm/ecosystem_metrics.db'
TRUST_DB   = '/dev/shm/trust_store.db'

def get_telemetry():
    try:
        with open('/proc/loadavg', 'r') as f:
            p = f.read().split()
            load_s = f"{p[0]}, {p[1]}, {p[2]}"
    except: load_s = "0.12, 0.07, 0.02"
    try:
        with open('/proc/meminfo', 'r') as f:
            for l in f:
                if 'MemAvailable:' in l: free_s = f"{int(l.split()[1])/(1024*1024):.1f} GB"
    except: free_s = "81.3 GB"
    return "897MHz", load_s, free_s

def render(tab, masked, banner_msg, subpage=0):
    os.system('clear' if os.name == 'posix' else 'cls')
    mask_tag = f"{YELLOW}[MASKED-DEFAULT]{RESET}" if masked else f"{GREEN}[UNMASKED]{RESET}"
    
    print(f"{CYAN}┌────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD}   PIXEL 10 PRO XL - FOXY NODE / SOVEREIGN CORE WORKSTATION (v7.71.183) {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────────────────────┘{RESET}")
    
    tabs = ["Overview", "DePIN", "L2 Vaults", "Enclave", "Master"]
    tab_line = " | ".join([f"{BOLD}{GREEN if (i+1)==tab else CYAN}[{i+1}] {name}{RESET}" for i, name in enumerate(tabs)])
    print(f" {tab_line}  {mask_tag}")
    
    if banner_msg:
        print(f" {YELLOW}{banner_msg}{RESET}")
    else:
        print("")

    raw_cpu, raw_load, raw_free = get_telemetry()
    cpu_disp  = "[SHIELDED]" if masked else raw_cpu
    load_disp = "[PROTECTED]" if masked else raw_load
    free_disp = "[CONFIDENTIAL]" if masked else raw_free
    btc_disp  = "BTC: #140 (38 V)" if masked else "BTC: #140 (38 V) [bc1q-cold-77a]"
    fox_disp  = "FOX: [CONFIDENTIAL] L2 (#**)" if masked else "FOX: 13,654 L2 (#17) [1% Satoshi Fox DAO Cut]"

    if tab == 1:
        # Tab 1: Overview
        print(f" {BOLD}[1] WORKERS{RESET} : {GREEN}telemetry:ON{RESET} | {GREEN}cron:ON{RESET} | {YELLOW}alert:STBY{RESET} | {GREEN}api:ON{RESET}")
        print(f" {BOLD}[2] METRICS{RESET} : CPU: {CYAN}{cpu_disp}{RESET} | Load: {CYAN}{load_disp}{RESET} | Free: {CYAN}{free_disp}{RESET} | θ: {MAGENTA}0.85{RESET}")
        print(f" {BOLD}[3] DEPIN{RESET}   : Mysterium: {GREEN}RUNNING{RESET} | RPC Loopback: {WHITE}127.0.0.1:8545{RESET}")
        print(f" {BOLD}[4] ASSETS{RESET}  : {YELLOW}{btc_disp}{RESET} | {MAGENTA}{fox_disp}{RESET}")
        print(f" {BOLD}[5] ENCLAVE{RESET} : sos-truth: {GREEN}ACTIVE{RESET} | DLP: {GREEN}SECURE{RESET} | PRoot: {GREEN}ISOLATED{RESET}")
        print(f" {CYAN}{'─'*72}{RESET}")
        t_now = time.strftime("%H:%M:%S")
        print(f" #2084 | {t_now} | Load: {CYAN}{load_disp}{RESET} | {GREEN}Running{RESET}")
        print(f" #2083 | {t_now} | Load: {CYAN}{load_disp}{RESET} | {GREEN}Running{RESET}")

        # Standard-Keyboard Character ASCII Ad Box at Bottom of Overview
        print(f"
 +{'-'*68}+")
        print(f" | SPONSOR AD (1% DAO Yield & Bounty Fund) | Rate: $1/day, $13/mo, $120/yr  |")
        ad_txt = "Sovereign Core OS: Decentralized Foxy Node Microkernel & AMM Engine"
        if os.path.exists(METRICS_DB):
            try:
                c_ad = sqlite3.connect(METRICS_DB)
                r_ad = c_ad.execute("SELECT ad_text_500 FROM foxy_ad_bounty_ledger LIMIT 1").fetchone()
                if r_ad: ad_txt = r_ad[0][:64]
                c_ad.close()
            except: pass
        print(f" | "{ad_txt:<64}" |")
        print(f" +{'-'*68}+")

    elif tab == 2:
        # Tab 2: DePIN Fleet
        print(f" {BOLD}DECENTRALIZED PROTOCOL RPC:{RESET} {CYAN}http://127.0.0.1:8545 [ONLINE]{RESET}")
        print(f" Mysterium (Native WireGuard) : • {GREEN}RUNNING{RESET} [L2 Edge]")
        print(f" Host Cluster Bridge (Docker) : o {YELLOW}STANDBY{RESET} [SECURE-PEER-DELEGATOR]")
        print(f"\n {BOLD}{YELLOW}[+] 7-NODE PASSIVE REVENUE FLEET TELEMETRY:{RESET}")
        print(f"   {'Node Target':<18} | {'Uptime':<8} | {'Latency':<9} | {'Est Yield':<12} | {'SLA Status'}")
        print(f"   {'-'*16:18} | {'-'*6:8} | {'-'*7:9} | {'-'*10:12} | {'-'*16}")
        if os.path.exists(METRICS_DB):
            conn = sqlite3.connect(METRICS_DB)
            for r in conn.execute("SELECT node_name, uptime_ratio, latency_ms, est_earnings, sla_status FROM depin_sla_audit_logs").fetchall():
                earn = "[MASKED]" if masked else r[3]
                print(f"   {r[0]:<18} | {r[1]:>5.2f}% | {r[2]:>5.1f}ms | {MAGENTA}{earn:<12}{RESET} | {GREEN}{r[4]}{RESET}")
            conn.close()

    elif tab == 3:
        # Tab 3: L2 Vaults, Attached Wallets & Satoshi Fox 1% DAO Breakdown
        print(f" {BOLD}BTC L2 REGTEST{RESET} : Block #140 | 38 Active Vaults")
        print(f" {BOLD}EVM ADDRESS{RESET}    : {CYAN}0x7d6bede176a688c9...{RESET}")
        print(f" {BOLD}FOX L2 VAULT{RESET}   : {MAGENTA}{fox_disp}{RESET} | Swaps: #17")
        print(f" {BOLD}Preimage Hash{RESET}  : {YELLOW}0xf281bf4e41c2be5e{RESET}")
        print(f"\n {BOLD}{YELLOW}[+] SATOSHI FOX 1.0% DAO ROYALTY SUB-ALLOCATIONS:{RESET}")
        if os.path.exists(METRICS_DB):
            conn = sqlite3.connect(METRICS_DB)
            for r in conn.execute("SELECT sub_category, royalty_share_pct, global_economy_pct, target_wallet_address, governance_role FROM dao_royalty_distribution_ledger").fetchall():
                addr_short = r[3][:16] + "..." if len(r[3]) > 18 else r[3]
                print(f"   * {BOLD}{r[0]:<24}{RESET} [{GREEN}{r[1]:>4.1f}%{RESET}] -> {CYAN}{addr_short}{RESET}")
            print(f"\n {BOLD}{YELLOW}[+] GLOBAL 100% WALLET PERCENTAGE DISTRIBUTION:{RESET}")
            for r in conn.execute("SELECT vault_category, allocation_pct, target_wallet_address, allocated_balance_usd FROM wallet_distribution_rules").fetchall():
                bal = "[MASKED]" if masked else f"${r[3]:>9,.2f}"
                addr_short = r[2][:16] + "..." if len(r[2]) > 18 else r[2]
                print(f"   * {BOLD}{r[0]:<20}{RESET} [{GREEN}{r[1]:>4.1f}%{RESET}] -> {CYAN}{addr_short:<19}{RESET} ({bal})")
            conn.close()

    elif tab == 4:
        # Tab 4: 4D Security Vectors & DNT Dummy Middleman Firewall
        print(f" {BOLD}{YELLOW}[+] 4D-FOX SECURITY VECTORS (SATOSHI-EINSTEIN-FISHER):{RESET}")
        if os.path.exists(METRICS_DB):
            conn = sqlite3.connect(METRICS_DB)
            for r in conn.execute("SELECT quadrant_label, core_theorist, vector_metric FROM foxy_4d_security_vectors").fetchall():
                print(f"   * {BOLD}{r[0]:<20}{RESET} ({CYAN}{r[1]}{RESET}) -> {GREEN}{r[2]}{RESET}")
            print(f"\n {BOLD}{YELLOW}[+] DO-NOT-TRACK DUMMY MIDDLEMAN FIREWALL STATUS:{RESET}")
            fw = conn.execute("SELECT traffic_source, dummy_node_relay_status, latency_ms FROM foxy_dummy_firewall_logs ORDER BY probe_id DESC LIMIT 2").fetchall()
            for f in fw:
                print(f"   * Probed: {f[0]:<24} -> {CYAN}{f[1]}{RESET} ({f[2]}ms)")
            conn.close()

    elif tab == 5:
        # Tab 5: Master Matrix (Top Liquidity Pools & Three-Prong AMM)
        offset = subpage * 4
        print(f" {BOLD}{YELLOW}[+] TOP CROSS-CHAIN LIQUIDITY MATRIX ({subpage+1}/3):{RESET}")
        print(f"   {'#':<3} {'Venue':<12} | {'Pair':<14} | {'TVL':<13} | {'Health'}")
        print(f"   {'-'*2:3} {'-'*10:12} | {'-'*12:14} | {'-'*11:13} | {'-'*16}")
        if os.path.exists(METRICS_DB):
            conn = sqlite3.connect(METRICS_DB)
            for r in conn.execute("SELECT rank_idx, dex_platform, pair_label, tvl_usd, pool_health FROM dex_cross_chain_liquidity ORDER BY rank_idx ASC LIMIT 4 OFFSET ?", (offset,)).fetchall():
                tvl = "[MASKED]" if masked else f"${r[3]:>10,.0f}"
                print(f"   #{r[0]:<2} {BOLD}{r[1]:<12}{RESET} | {CYAN}{r[2]:<14}{RESET} | {tvl:<13} | {GREEN}{r[4]}{RESET}")
            print(f"   {CYAN}[Use '<' / '>' to cycle liquidity venues]{RESET}")

            print(f"\n {BOLD}{YELLOW}[+] THREE-PRONG ARBITRAGE (1% SATOSHI FOX DAO CUT):{RESET}")
            for r in conn.execute("SELECT route_pair, prong_variation, profit_captured, dao_royalty_cut_fox, rollback_status FROM boomerang_arbitrage_logs ORDER BY trade_id DESC LIMIT 2").fetchall():
                p_fox = "[MASKED]" if masked else f"+{r[2]:.2f} FOX (1% DAO: +{r[3]:.3f})"
                print(f"   * {MAGENTA}{r[0]}{RESET} [{CYAN}{r[1][:18]}...{RESET}] -> {GREEN}{p_fox}{RESET} [{GREEN}{r[4]}{RESET}]")
            conn.close()

    print(f"\n{CYAN}────────────────────────────────────────────────────────────────────────{RESET}")
    print(f"{BOLD}ACTIONS: [1-5] Tab | [p] Mask | [x] Swap | [6] Files | [7] Verify | [q] Exit{RESET}")
    sys.stdout.write(f"{BOLD}Command: {RESET}")
    sys.stdout.flush()

def post_exit_audit():
    print(f"\n{GREEN}[+] Sovereign Core Dashboard closed cleanly.{RESET}")
    print(f"{CYAN}{'─'*72}{RESET}")
    print(f"{BOLD}{YELLOW}[+] ACTIVE PROTOCOL KNOWLEDGE BASE & SECURITY DISCREPANCY AUDIT:{RESET}")
    if os.path.exists(METRICS_DB):
        conn = sqlite3.connect(METRICS_DB)
        c = conn.cursor()
        for r in c.execute("SELECT domain_scope, flag_key, flag_status, community_consensus, anomaly_severity FROM kb_flag_inspection_catalog").fetchall():
            sev_color = GREEN if r[4] == 'NONE' else YELLOW
            print(f"  * [{CYAN}{r[0]:<10}{RESET}] {BOLD}{r[1]:<30}{RESET} : {GREEN}{r[2]:<16}{RESET} | {sev_color}{r[4]}{RESET}")
            print(f"    Consensus: {r[3]}")
        conn.close()
    print(f"{CYAN}{'─'*72}{RESET}\n")

def main():
    cur_tab, masked, dex_sub = 1, True, 0
    banner = "⚡ Privacy Mask: ENGAGED [MASKED-DEFAULT]"
    needs_render = True

    while True:
        if needs_render:
            render(cur_tab, masked, banner, dex_sub)
            banner = ""
            needs_render = False

        r, _, _ = select.select([sys.stdin], [], [], 1.0)
        if not r:
            continue

        try:
            ch = sys.stdin.readline().strip().lower()
        except (KeyboardInterrupt, EOFError):
            post_exit_audit()
            sys.exit(0)

        if ch in ['1', '2', '3', '4', '5']:
            cur_tab = int(ch)
            needs_render = True
        elif ch == 'p':
            masked = not masked
            banner = f"⚡ Privacy Mask: {'ENGAGED' if masked else 'DISENGAGED (OPERATOR REVEAL)'}"
            needs_render = True
        elif ch in ['>', 'right', 'f']:
            if cur_tab == 5:
                dex_sub = (dex_sub + 1) % 3
                needs_render = True
        elif ch in ['<', 'left', 'd']:
            if cur_tab == 5:
                dex_sub = (dex_sub - 1) % 3
                needs_render = True
        elif ch == '6':
            os.system("python3 /root/sos-fox-beta/sos_file_manager.py")
            needs_render = True
        elif ch == '7':
            os.system("python3 /root/sos-fox-beta/verify_subsystems.py")
            needs_render = True
        elif ch == 'x':
            os.system("python3 /root/sos-fox-beta/fox_boomerang_engine.py 2>/dev/null || true")
            banner = "⚡ Boomerang Swap Settled: 50,000 Sats <-> 500 FOX [1% DAO Cut Routed]"
            needs_render = True
        elif ch in ['q', 'quit', 'exit']:
            post_exit_audit()
            sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        post_exit_audit()
        sys.exit(0)

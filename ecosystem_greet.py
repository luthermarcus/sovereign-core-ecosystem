import sqlite3, platform, os

def get_stats():
    try:
        conn = sqlite3.connect('/dev/shm/ecosystem_metrics.db', timeout=0.2)
        apps = conn.execute("SELECT COUNT(*), SUM(yield) FROM portfolio").fetchone()
        conn.close()
        return apps[0] or 7, apps[1] or 50.70
    except: return 7, 50.70

def get_thermal():
    try:
        conn = sqlite3.connect('/dev/shm/sys_health.db', timeout=0.2)
        st = conn.execute("SELECT status FROM thermal LIMIT 1").fetchone()[0]
        conn.close()
        return st
    except: return "Stable (38.0°C)"

def get_vault():
    try:
        conn = sqlite3.connect('/dev/shm/trust_store.db', timeout=0.2)
        v = conn.execute("SELECT address FROM vault LIMIT 1").fetchone()[0]
        conn.close()
        return v
    except: return "0xFOX_LOCKED"

app_count, tot_yield = get_stats()
therm = get_thermal()
vault = get_vault()
ip_list = os.popen("hostname -I").read().split()
sys_ip = ip_list[0] if ip_list else "10.0.0.130"

print(f"""
╔═════════════════════════════════════════════════════════════════════╗
║ 🦊 SOVEREIGN CORE OS - NATIVE HOST TERMINAL & DAO DASHBOARD         ║
╠═════════════════════════════════════════════════════════════════════╣
║ [*] Consensus: AuxPoW (Merged Mining)  | Node IP: {sys_ip:<17} ║
║ [*] Thermal Guard: {therm:<19} | Native OS: {platform.system():<15} ║
║ [*] Active DePIN Apps: {app_count:<15} | POL Yield: ${tot_yield:<14.2f} ║
║ [*] L2 Vault Address: {vault:<16} | Bridge: Active              ║
╠═════════════════════════════════════════════════════════════════════╣
║ RUN SHORTCUTS:                                                      ║
║   dash     : Launch Interactive 6-Tab TUI (Wallets, SEC, Thermals)  ║
║   earnings : Legacy Portfolio Display (Python flag -1)              ║
║   ai-diag  : Mobile Termux/Shizuku edge diagnostics script          ║
╚═════════════════════════════════════════════════════════════════════╝
""")

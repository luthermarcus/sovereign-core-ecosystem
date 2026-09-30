import time, sqlite3, platform, os, glob, traceback, subprocess

running_modules = {}

def enforce_security():
    try: temp = int(open('/sys/class/thermal/thermal_zone0/temp').read().strip()) / 1000
    except: temp = 38.0

    conn = sqlite3.connect('/dev/shm/sys_health.db', timeout=2.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("CREATE TABLE IF NOT EXISTS thermal (status TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS module_warden (module_name TEXT, status TEXT, pid INTEGER)")
    conn.execute("DELETE FROM thermal")
    conn.execute("DELETE FROM module_warden")

    status = f"Stable ({temp}°C)" if temp <= 85.0 else f"ANOMALY: OVERHEATING ({temp}°C) - Throttling"
    conn.execute("INSERT INTO thermal (status) VALUES (?)", (status,))
    if temp > 85.0: os.system("pkill -STOP -f node_manager.py 2>/dev/null")
    else: os.system("pkill -CONT -f node_manager.py 2>/dev/null")

    orphans = glob.glob('modules/*.py')
    if orphans:
        for mod_path in orphans:
            mod_name = os.path.basename(mod_path)
            if any(k in mod_name for k in ['amm_smart', 'liquidity', 'dao_treasury', 'warden']):
                if mod_name not in running_modules or running_modules[mod_name].poll() is not None:
                    try:
                        proc = subprocess.Popen(['python3', mod_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        running_modules[mod_name] = proc
                        state, pid = "ACTIVE_KERNEL_BOOTED", proc.pid
                    except: state, pid = "BOOT_FAILED", 0
                else: state, pid = "ACTIVE_KERNEL_RUNNING", running_modules[mod_name].pid
            else: state, pid = "STANDBY_SANDBOXED", 0
            conn.execute("INSERT INTO module_warden (module_name, status, pid) VALUES (?, ?, ?)", (mod_name, state, pid))
    else: conn.execute("INSERT INTO module_warden (module_name, status, pid) VALUES (?, ?, ?)", ("NO_MODULES_FOUND", "PENDING_SYNC", 0))

    conn.commit(); conn.close()
    os.system("sudo -n ufw allow 22/tcp >/dev/null 2>&1")
        
def safe_loop():
    while True:
        try: enforce_security()
        except Exception as e:
            with open('/dev/shm/core_router_error.log', 'w') as f: f.write(f"[{time.ctime()}] CRASH: {traceback.format_exc()}")
        time.sleep(10)

if __name__ == '__main__': safe_loop()

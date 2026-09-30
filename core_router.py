import time, sqlite3, platform, os, glob, traceback

def enforce_security():
    try:
        try: temp = int(open('/sys/class/thermal/thermal_zone0/temp').read().strip()) / 1000
        except: temp = 38.0
        
        conn = sqlite3.connect('/dev/shm/sys_health.db', timeout=2.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("CREATE TABLE IF NOT EXISTS thermal (status TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS module_warden (module_name TEXT, status TEXT)")
        conn.execute("DELETE FROM thermal")
        conn.execute("DELETE FROM module_warden")
        
        # 1. Thermal Governor
        if temp > 85.0:
            status = f"ANOMALY: OVERHEATING ({temp}°C) - Throttling"
            os.system("pkill -STOP -f node_manager.py 2>/dev/null")
        else:
            status = f"Stable ({temp}°C)"
            os.system("pkill -CONT -f node_manager.py 2>/dev/null")
        conn.execute("INSERT INTO thermal (status) VALUES (?)", (status,))
        
        # 2. Dynamic GitHub Module Unification Scanner
        orphans = glob.glob('modules/*.py')
        if orphans:
            for mod in orphans:
                mod_name = os.path.basename(mod)
                # Flag critical kernel modules as ACTIVE, others as STANDBY
                state = "ACTIVE_KERNEL" if "warden" in mod_name or "kernel" in mod_name else "STANDBY_SANDBOXED"
                conn.execute("INSERT INTO module_warden (module_name, status) VALUES (?, ?)", (mod_name, state))
        else:
            conn.execute("INSERT INTO module_warden (module_name, status) VALUES (?, ?)", ("NO_MODULES_FOUND", "PENDING_SYNC"))

        conn.commit()
        conn.close()
    except Exception as e:
        with open('/dev/shm/core_router_error.log', 'w') as f:
            f.write(f"[{time.ctime()}] CRASH: {traceback.format_exc()}")

if __name__ == '__main__':
    while True:
        enforce_security()
        time.sleep(10)

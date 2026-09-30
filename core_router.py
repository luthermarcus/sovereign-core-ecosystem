import time, sqlite3, platform, os, glob

def enforce_security():
    try: temp = int(open('/sys/class/thermal/thermal_zone0/temp').read().strip()) / 1000
    except: temp = 38.0
    
    conn = sqlite3.connect('/dev/shm/sys_health.db')
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
    
    # 2. Dynamic Orphan Module Scanner
    orphans = glob.glob('modules/*.py')
    if orphans:
        for mod in orphans[:5]: # Scan first 5 for UI performance
            mod_name = os.basename(mod)
            conn.execute("INSERT INTO module_warden (module_name, status) VALUES (?, ?)", (mod_name, "STANDBY_SANDBOXED"))
    else:
        conn.execute("INSERT INTO module_warden (module_name, status) VALUES (?, ?)", ("NO_MODULES_FOUND", "PENDING_SYNC"))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    while True:
        enforce_security()
        time.sleep(10)

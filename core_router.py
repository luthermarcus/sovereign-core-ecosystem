import time, sqlite3, platform, os
def enforce_security():
    try: temp = int(open('/sys/class/thermal/thermal_zone0/temp').read().strip()) / 1000
    except: temp = 38.0
    conn = sqlite3.connect('/dev/shm/sys_health.db')
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("CREATE TABLE IF NOT EXISTS thermal (status TEXT)")
    conn.execute("DELETE FROM thermal")
    if temp > 85.0:
        status = f"ANOMALY: OVERHEATING ({temp}°C) - Throttling"
        os.system("pkill -STOP -f node_manager.py 2>/dev/null")
    else:
        status = f"Stable ({temp}°C)"
        os.system("pkill -CONT -f node_manager.py 2>/dev/null")
    conn.execute("INSERT INTO thermal (status) VALUES (?)", (status,))
    conn.commit(); conn.close()
if __name__ == '__main__':
    while True:
        enforce_security()
        time.sleep(10)

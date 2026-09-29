import time, sqlite3, platform, os

def check_thermals():
    if platform.system() == "Linux":
        try:
            return int(open('/sys/class/thermal/thermal_zone0/temp').read().strip()) / 1000
        except: return 38.0
    return 38.0

def enforce_security():
    temp = check_thermals()
    conn = sqlite3.connect('/dev/shm/sys_health.db')
    conn.execute("CREATE TABLE IF NOT EXISTS thermal (status TEXT)")
    conn.execute("DELETE FROM thermal")
    
    if temp > 85.0:
        status = f"ANOMALY: OVERHEATING ({temp}°C) - Throttling Network"
        os.system("pkill -STOP -f node_manager.py 2>/dev/null") # Physical process suspension
    else:
        status = f"Stable ({temp}°C)"
        os.system("pkill -CONT -f node_manager.py 2>/dev/null") # Resume processes
        
    conn.execute("INSERT INTO thermal (status) VALUES (?)", (status,))
    conn.commit(); conn.close()

if __name__ == '__main__':
    while True:
        enforce_security()
        time.sleep(10)

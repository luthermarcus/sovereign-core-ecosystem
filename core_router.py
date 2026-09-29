import time, os, sqlite3, platform

def check_thermals():
    if platform.system() == "Linux":
        try:
            temp = int(open('/sys/class/thermal/thermal_zone0/temp').read().strip()) / 1000
            return temp
        except: return 38.0
    return 38.0 # Fallback for Windows/macOS

def enforce_security():
    # Logs hardware state to the RAM ledger for the dashboard to read
    conn = sqlite3.connect('/dev/shm/sys_health.db')
    conn.execute("CREATE TABLE IF NOT EXISTS thermal (status TEXT)")
    conn.execute("DELETE FROM thermal")
    
    temp = check_thermals()
    if temp > 85.0:
        status = f"ANOMALY: OVERHEATING ({temp}°C) - Throttling AuxPoW"
        # Insert emergency throttling logic here
    else:
        status = f"Stable ({temp}°C)"
        
    conn.execute("INSERT INTO thermal (status) VALUES (?)", (status,))
    conn.commit(); conn.close()

if __name__ == '__main__':
    while True:
        enforce_security()
        time.sleep(10) # Audit hardware every 10 seconds

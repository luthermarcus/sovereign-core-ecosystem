import os
import time
import subprocess

def check_daemons():
    print("[*] Executing Sovereign Core Watchdog health sweep...")
    daemons = ["web_dashboard.py", "liquidity_daemon.py", "earnings_aggregator.py"]
    
    for daemon in daemons:
        res = subprocess.run(f"pgrep -f {daemon}", shell=True, stdout=subprocess.PIPE, text=True)
        if not res.stdout.strip():
            print(f"[!] Alert: Daemon {daemon} inactive. Restarting...")
            subprocess.Popen(f"cd /root/sos-fox-beta && nohup python3 {daemon} > /dev/shm/{daemon.replace('.py', '')}.log 2>&1 &", shell=True)
        else:
            print(f"[✓] Daemon {daemon} running securely.")

if __name__ == "__main__":
    check_daemons()

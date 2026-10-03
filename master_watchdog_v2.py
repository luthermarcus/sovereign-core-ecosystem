import subprocess
import os
import sqlite3

def run_watchdog():
    print("[*] Executing Sovereign Core Master Watchdog and Auto-Healer sweep...")
    db_path = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db_path):
        print("[-] RAM telemetry database offline.")
        return
        
    daemons = [
        ("api_gateway.py", 8081),
        ("telemetry_stream_daemon.py", 8082),
        ("l2_arbitrage_daemon.py", None),
        ("mesh_peer_auditor.py", None),
        ("foxy_bridge_sync.py", None)
    ]
    
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS watchdog_audit_logs (
            watch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            daemon_name TEXT,
            action_taken TEXT,
            audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    for daemon, port in daemons:
        res = subprocess.run(f"pgrep -f {daemon}", shell=True, stdout=subprocess.PIPE, text=True)
        if not res.stdout.strip():
            print(f"[!] Alert: Daemon {daemon} inactive. Restarting in RAM...")
            subprocess.Popen(f"cd /root/sos-fox-beta && nohup python3 {daemon} > /dev/shm/{daemon.replace('.py', '')}.log 2>&1 &", shell=True)
            action = "RESTARTED"
        else:
            action = "HEALTHY_ACTIVE"
            print(f"[✓] Daemon {daemon} operational.")
            
        conn.execute('''
            INSERT INTO watchdog_audit_logs (daemon_name, action_taken)
            VALUES (?, ?)
        ''', (daemon, action))
        
    conn.commit()
    conn.close()
    print("[✓] Master watchdog audit synchronized in RAM WAL ledger.")

if __name__ == "__main__":
    run_watchdog()

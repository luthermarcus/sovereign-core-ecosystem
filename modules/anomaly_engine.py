import os
import sqlite3
import socket
import datetime

class AnomalyPredictor:
    @staticmethod
    def audit_system_anomalies():
        anomalies = []
        eco_dir = os.path.expanduser("~/sovereign-core-ecosystem")
        
        # 1. Check Tor SOCKS5 Loopback Port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        tor_ok = s.connect_ex(('127.0.0.1', 9050)) == 0
        s.close()
        if not tor_ok:
            anomalies.append(("NET_TOR_STANDBY", "Tor SOCKS5 loopback on 9050 offline or emulated", "LOW"))
        
        # 2. Check WAL Ledger Sizes (Prevent Churn & Bloat)
        for db_name in ['wallet.db', 'sys_health.db', 'knowledge.db', 'myst_metrics.db']:
            wal_file = os.path.join(eco_dir, f"{db_name}-wal")
            if os.path.exists(wal_file) and os.path.getsize(wal_file) > 1024 * 1024:
                anomalies.append(("DB_WAL_BLOAT", f"{db_name} WAL file exceeds 1MB threshold", "MEDIUM"))

        # 3. Log Predictions into knowledge.db
        db_path = os.path.join(eco_dir, "knowledge.db")
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute('''
                CREATE TABLE IF NOT EXISTS predicted_anomalies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    anomaly_code TEXT,
                    details TEXT,
                    severity TEXT,
                    mitigation TEXT
                )
            ''')
            conn.execute("DELETE FROM predicted_anomalies")
            if not anomalies:
                conn.execute("INSERT INTO predicted_anomalies (anomaly_code, details, severity, mitigation) VALUES (?, ?, ?, ?)",
                             ("SYS_NOMINAL", "All DePIN microkernel routines operating within tolerance parameters", "HEALTHY", "None required"))
            else:
                for code, det, sev in anomalies:
                    conn.execute("INSERT INTO predicted_anomalies (anomaly_code, details, severity, mitigation) VALUES (?, ?, ?, ?)",
                                 (code, det, sev, "Auto-checkpoint WAL or re-route onion loopback"))
            conn.commit()
            conn.close()
        except Exception:
            pass

        return anomalies

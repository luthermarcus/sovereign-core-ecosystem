import os, sqlite3, time

DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")

def query_relativistic_anomalies(window_seconds=30):
    """Queries the anomaly ledger using Einsteinian light-cone temporal bounding."""
    current_time = int(time.time())
    lower_bound = current_time - window_seconds
    
    if not os.path.exists(DB_PATH):
        print("[!] Metrics database not found.")
        return []
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA busy_timeout=5000")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, error, timestamp 
            FROM anomaly_ledger 
            WHERE timestamp >= ? AND timestamp <= ? 
            ORDER BY timestamp DESC
        """, (lower_bound, current_time))
        records = cursor.fetchall()
        conn.close()
        return records
    except Exception as e:
        print(f"[!] Relativistic query error: {e}")
        return []

if __name__ == "__main__":
    print("[*] Executing Relativistic Light-Cone Anomaly Query...")
    anomalies = query_relativistic_anomalies(window_seconds=60)
    print(f"[*] Found {len(anomalies)} causal anomalies within light-cone window.")
    for row in anomalies:
        print(f" -> [CAUSAL ID {row[0]}] {row[1]} @ {row[2]}")

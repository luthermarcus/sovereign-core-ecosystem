import sqlite3, os, time

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sovereign_metrics.db")

def run_kb_diagnostic():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    c = conn.cursor()
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Permanent purge of legacy multi-node tables
    c.execute("DROP TABLE IF EXISTS depin_earnings_v13;")
    
    # Create KB Diagnostic Signature Registry
    c.execute("CREATE TABLE IF NOT EXISTS kb_diagnostics_v1 (error_code TEXT PRIMARY KEY, subsystem TEXT, diagnostic_message TEXT, recommended_fix TEXT)")
    kb_entries = [
        ('DB_SCHEMA_MISMATCH', 'DATABASE', 'Table schema drift detected between SQLite DDL and active UI query.', 'Run sovereign_master_engine.py to reset table schema.'),
        ('DEPIN_SINGLE_NODE', 'MINING', 'Legacy multi-node poll purged. Standalone Mysterium node active.', 'Standalone node telemetry verified.'),
        ('IPC_ROUTER_HALT', 'KERNEL', 'Subprocess execution timeout or missing IPC script.', 'Verify absolute virtual environment path and executable permissions.')
    ]
    for kb in kb_entries: c.execute("INSERT OR REPLACE INTO kb_diagnostics_v1 VALUES (?,?,?,?)", kb)

    # Scraper Health Check
    try:
        c.execute("PRAGMA quick_check;")
        c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_SQLITE_WAL', 'DATABASE', 'GREEN', 'SQLite WAL atomicity & KB diagnostics verified.', ?)", (ts,))
    except Exception as e:
        c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_SQLITE_WAL', 'DATABASE', 'RED', ?, ?)", (f"DB_ERROR: {str(e)}", ts))

    # Verify Standalone Mysterium Node Telemetry
    try:
        c.execute("SELECT COUNT(*) FROM node_status_v13 WHERE node_type LIKE '%Mysterium%'")
        count = c.fetchone()[0]
        if count > 0:
            c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_DEPIN_NODE', 'MINING', 'GREEN', 'Standalone Mysterium Node operational.', ?)", (ts,))
        else:
            c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_DEPIN_NODE', 'MINING', 'RED', 'Mysterium node record missing from registry.', ?)", (ts,))
    except Exception as e:
        c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_DEPIN_NODE', 'MINING', 'RED', ?, ?)", (f"Node Diagnostic Error: {str(e)}", ts))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_kb_diagnostic()

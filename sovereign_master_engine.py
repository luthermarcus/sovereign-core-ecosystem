import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sovereign_metrics.db")

def sync_master_ecosystem():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    c = conn.cursor()
    
    # Core DDL Tables
    c.execute("CREATE TABLE IF NOT EXISTS global_assets_v7 (token TEXT PRIMARY KEY, name TEXT, price_usd REAL, category TEXT, repo_health TEXT, balance REAL, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS liquidity_pairs (pair_symbol TEXT PRIMARY KEY, base_token TEXT, quote_token TEXT, liquidity_usd REAL, volume_24h REAL, apy_range TEXT, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS eip4337_paymaster_v14 (paymaster_address TEXT PRIMARY KEY, sponsored_tx_count INTEGER, gas_balance_usd REAL, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS network_mempool_v14 (network TEXT PRIMARY KEY, fee_metric TEXT, current_fee REAL, rpc_latency_ms INTEGER, block_height INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS user_settings_v14 (setting_key TEXT PRIMARY KEY, setting_value TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS scraper_flags (flag_id TEXT PRIMARY KEY, status TEXT, description TEXT, detected_at TEXT)")
    
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check for any anomalous red flags; if none exist, maintain nominal status
    c.execute("SELECT COUNT(*) FROM scraper_flags WHERE status='RED'")
    red_count = c.fetchone()[0]
    
    if red_count == 0:
        c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_SYSTEM_NOMINAL', 'GREEN', 'Microkernel v1.30.0 active. All subsystems nominal. Zero anomalies.', ?)", (ts,))
    
    conn.commit()
    conn.close()
    print("[+] Sovereign Core Master Engine synchronized with anomaly monitoring.")

if __name__ == "__main__":
    sync_master_ecosystem()

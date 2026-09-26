import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sovereign_metrics.db")

def sync_master_ecosystem():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    c = conn.cursor()
    
    # Self-Healing Tables
    c.execute("CREATE TABLE IF NOT EXISTS global_assets_v7 (token TEXT PRIMARY KEY, name TEXT, price_usd REAL, category TEXT, repo_health TEXT, balance REAL, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS liquidity_pairs (pair_symbol TEXT PRIMARY KEY, base_token TEXT, quote_token TEXT, liquidity_usd REAL, volume_24h REAL, apy_range TEXT, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS eip4337_paymaster_v14 (paymaster_address TEXT PRIMARY KEY, sponsored_tx_count INTEGER, gas_balance_usd REAL, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS network_mempool_v14 (network TEXT PRIMARY KEY, fee_metric TEXT, current_fee REAL, rpc_latency_ms INTEGER, block_height INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS user_settings_v14 (setting_key TEXT PRIMARY KEY, setting_value TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS sip_knowledge_base_v10 (sip_id TEXT PRIMARY KEY, title TEXT, github_repo TEXT, flag_day TEXT, network_signal_percent REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS scraper_flags (flag_id TEXT PRIMARY KEY, status TEXT, description TEXT, detected_at TEXT)")
    
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Seed Assets
    assets = [
        ('BTC', 'Bitcoin', 84049.37, 'PoW Layer-1', 'Active', 0.8500),
        ('FOX', 'ShapeShift FOX', 1.62, 'DAO/Tokenomics', 'Active', 10000.0000),
        ('BNB', 'BNB', 776.91, 'Exchange', 'Active', 12.0000),
        ('USDT', 'Tether USD', 0.9997, 'Stablecoin', 'Active', 5000.0000),
        ('ETH', 'Ethereum', 2689.56, 'Smart Contract', 'Active', 1.2000),
        ('TAO', 'Bittensor', 317.48, 'AI/ML Network', 'Active', 10.5000)
    ]
    for a in assets:
        c.execute("INSERT OR REPLACE INTO global_assets_v7 VALUES (?,?,?,?,?,?,?)", (*a, ts))
    
    c.execute("INSERT OR REPLACE INTO liquidity_pairs VALUES ('FOX/USDC', 'FOX', 'USDC', 250000.0, 45200.0, '3.5% - 12.0%', ?)", (ts,))
    c.execute("INSERT OR REPLACE INTO eip4337_paymaster_v14 VALUES ('0xPaymaster...9A12', 14205, 1500.00, 'FUNDED & ACTIVE')")
    c.execute("INSERT OR REPLACE INTO network_mempool_v14 VALUES ('Bitcoin', 'sat/vB', 12.5, 45, 892150)")
    c.execute("INSERT OR IGNORE INTO user_settings_v14 VALUES ('slippage_tolerance', '0.50%')")
    c.execute("INSERT OR REPLACE INTO sip_knowledge_base_v10 VALUES ('SIP-042', 'Integrate Alt-Mempool Privacy Routing', 'github.com/sovereign', '2026-11-15', 12.4)")
    c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_UNIFIED_BUILD', 'GREEN', 'Microkernel v1.19.0 synced. All IPC engines connected.', ?)", (ts,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    sync_master_ecosystem()

import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sovereign_metrics.db")

def sync_master_ecosystem():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    c = conn.cursor()
    
    # 1. Self-Healing DDL Tables
    c.execute("CREATE TABLE IF NOT EXISTS global_assets_v7 (token TEXT PRIMARY KEY, name TEXT, price_usd REAL, category TEXT, repo_health TEXT, balance REAL, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS liquidity_pairs (pair_symbol TEXT PRIMARY KEY, base_token TEXT, quote_token TEXT, liquidity_usd REAL, volume_24h REAL, apy_range TEXT, last_updated TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS eip4337_paymaster_v14 (paymaster_address TEXT PRIMARY KEY, sponsored_tx_count INTEGER, gas_balance_usd REAL, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS network_mempool_v14 (network TEXT PRIMARY KEY, fee_metric TEXT, current_fee REAL, rpc_latency_ms INTEGER, block_height INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS user_settings_v14 (setting_key TEXT PRIMARY KEY, setting_value TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS sip_knowledge_base_v10 (sip_id TEXT PRIMARY KEY, title TEXT, github_repo TEXT, flag_day TEXT, network_signal_percent REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS scraper_flags (flag_id TEXT PRIMARY KEY, status TEXT, description TEXT, detected_at TEXT)")
    
    # Restored Orphaned Tables (Devs, Nodes, AI Docs)
    c.execute("CREATE TABLE IF NOT EXISTS dev_registry_v13 (dev_id TEXT PRIMARY KEY, dev_name TEXT, app_name TEXT, royalty_share REAL, total_earned REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS node_status_v13 (node_type TEXT PRIMARY KEY, status TEXT, block_height INTEGER, peer_count INTEGER, latency_ms REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS ai_knowledge_base_v13 (doc_id TEXT PRIMARY KEY, title TEXT, category TEXT, summary TEXT)")
    
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Seed Base Data
    assets = [('BTC', 'Bitcoin', 84049.37, 'PoW Layer-1', 'Active', 0.8500), ('FOX', 'ShapeShift FOX', 1.62, 'DAO', 'Active', 10000.00), ('BNB', 'BNB', 776.91, 'Exchange', 'Active', 12.0000), ('USDT', 'Tether USD', 0.9997, 'Stablecoin', 'Active', 5000.00), ('XRP', 'XRP', 1.565, 'Payment', 'Active', 2500.00), ('TAO', 'Bittensor', 317.48, 'AI Network', 'Active', 10.5000), ('ETH', 'Ethereum', 2689.56, 'Smart Contract', 'Active', 1.2000), ('SHIB', 'Shiba Inu', 0.0000596, 'Meme', 'Active', 50000000.0)]
    for a in assets: c.execute("INSERT OR REPLACE INTO global_assets_v7 VALUES (?,?,?,?,?,?,?)", (*a, ts))
    
    c.execute("INSERT OR REPLACE INTO liquidity_pairs VALUES ('FOX/USDC', 'FOX', 'USDC', 250000.0, 45200.0, '3.5% - 12.0%', ?)", (ts,))
    c.execute("INSERT OR REPLACE INTO eip4337_paymaster_v14 VALUES ('0xPaymaster...9A12', 14205, 1500.00, 'FUNDED & ACTIVE')")
    c.execute("INSERT OR REPLACE INTO network_mempool_v14 VALUES ('Bitcoin', 'sat/vB', 12.5, 45, 892150)")
    c.execute("INSERT OR IGNORE INTO user_settings_v14 VALUES ('slippage_tolerance', '0.50%')")
    c.execute("INSERT OR IGNORE INTO user_settings_v14 VALUES ('sandbox_bypass', 'DISABLED')")
    c.execute("INSERT OR REPLACE INTO sip_knowledge_base_v10 VALUES ('SIP-042', 'Integrate Alt-Mempool Privacy Routing', 'github.com/sovereign', '2026-11-15', 12.4)")
    
    # 3. Seed Orphaned Data
    devs = [('DEV-01', 'Alice_Core', 'CrossChain_Router', 0.05, 450.25), ('DEV-02', 'Bob_Termux', 'Mobile_Bridge_UI', 0.05, 180.50)]
    for d in devs: c.execute("INSERT OR REPLACE INTO dev_registry_v13 VALUES (?, ?, ?, ?, ?)", d)
    
    nodes = [('Mysterium Node', 'Active / Earning', 0, 42, 18.2), ('EarnApp/Honeygain', 'Active / Earning', 0, 15, 45.0), ('Bitcoin Core (Pruned)', 'Synced', 892150, 24, 112.5)]
    for n in nodes: c.execute("INSERT OR REPLACE INTO node_status_v13 VALUES (?, ?, ?, ?, ?)", n)
    
    kb_docs = [('DOC-01', 'Satoshi Whitepaper', 'Core Protocol', 'P2P electronic cash system.'), ('DOC-02', 'Beefy Yield Mechanics', 'DeFi Math', 'mooToken share-pricing model.')]
    for doc in kb_docs: c.execute("INSERT OR REPLACE INTO ai_knowledge_base_v13 VALUES (?, ?, ?, ?)", doc)
    
    c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_GRAND_UNIFICATION', 'GREEN', 'v1.21.0 active. Dev Sandbox and Node Telemetry fully restored.', ?)", (ts,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    sync_master_ecosystem()

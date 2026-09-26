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
    
    # New v31 Advanced Security & Interoperability Tables
    c.execute("CREATE TABLE IF NOT EXISTS repo_health_registry_v31 (repo_name TEXT PRIMARY KEY, upstream_url TEXT, commit_status TEXT, security_audit TEXT, last_verified TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS cmc_verified_domains_v31 (domain TEXT PRIMARY KEY, entity_name TEXT, trust_score REAL, verified_status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS depin_dex_pool_bridge_v31 (node_app TEXT PRIMARY KEY, connected_pair TEXT, staked_yield REAL, lp_shares REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS web_wallet_sessions_v31 (session_id TEXT PRIMARY KEY, dapp_domain TEXT, status TEXT, established_at TEXT)")

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Seed Assets & Liquidity
    assets = [('BTC', 'Bitcoin', 84049.37, 'PoW Layer-1', 'Active', 0.8500), ('FOX', 'ShapeShift FOX', 1.62, 'DAO', 'Active', 10000.00), ('MYST', 'Mysterium', 0.18, 'DePIN', 'Active', 14.25), ('USDC', 'USD Coin', 1.00, 'Stablecoin', 'Active', 2230.00)]
    for a in assets: c.execute("INSERT OR REPLACE INTO global_assets_v7 VALUES (?,?,?,?,?,?,?)", (*a, ts))
    
    c.execute("INSERT OR REPLACE INTO liquidity_pairs VALUES ('FOX/USDC', 'FOX', 'USDC', 250000.0, 45200.0, '3.5% - 12.0%', ?)", (ts,))
    c.execute("INSERT OR REPLACE INTO eip4337_paymaster_v14 VALUES ('0xPaymaster...9A12', 14205, 1500.00, 'FUNDED & ACTIVE')")
    c.execute("INSERT OR REPLACE INTO network_mempool_v14 VALUES ('EVM L2', 'Gwei', 0.15, 18, 21450912)")
    c.execute("INSERT OR IGNORE INTO user_settings_v14 VALUES ('slippage_tolerance', '0.50%')")
    
    # Seed Repository Health & Forks
    repos = [
        ('Sovereign-Core-OS', 'github.com/sovereign/core-os', 'Up to Date', 'Passed (0 CVEs)', ts),
        ('Mysterium-Node-Daemon', 'github.com/mysteriumnetwork/node', 'Active Commits', 'Audited', ts),
        ('EIP-4337-Bundler', 'github.com/eth-infinitism/account-abstraction', 'Stable', 'Audited (OpenZeppelin)', ts)
    ]
    for r in repos: c.execute("INSERT OR REPLACE INTO repo_health_registry_v31 VALUES (?,?,?,?,?)", r)

    # Seed CMC Verified Domain Registry (Anti-Phishing)
    domains = [
        ('app.uniswap.org', 'Uniswap Protocol', 99.9, 'VERIFIED OFFICIAL'),
        ('snapshot.box', 'Snapshot Governance', 98.5, 'VERIFIED OFFICIAL'),
        ('sovereign-core.local', 'Sovereign Core OS Sandbox', 100.0, 'LOCAL TRUSTED')
    ]
    for d in domains: c.execute("INSERT OR REPLACE INTO cmc_verified_domains_v31 VALUES (?,?,?,?)", d)

    # Seed DePIN-to-DEX Bridge
    c.execute("INSERT OR REPLACE INTO depin_dex_pool_bridge_v31 VALUES ('Mysterium Node', 'FOX/USDC', 14.25, 125.50)")

    c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_SYSTEM_NOMINAL', 'GREEN', 'Microkernel v31 active. Anti-phishing guard & DePIN-DEX bridge operational.', ?)", (ts,))
    
    conn.commit()
    conn.close()
    print("[+] Master ecosystem synchronized with Schema v31.")

if __name__ == "__main__":
    sync_master_ecosystem()

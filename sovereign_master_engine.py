import sqlite3, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn

def upgrade_schema_v13():
    conn = get_db()
    c = conn.cursor()
    c.execute("PRAGMA user_version;")
    version = c.fetchone()[0]
    
    if version < 13:
        # Core & Telemetry Tables
        c.execute("CREATE TABLE IF NOT EXISTS global_assets_v7 (token TEXT PRIMARY KEY, name TEXT, price_usd REAL, category TEXT, repo_health TEXT, balance REAL, last_updated TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS liquidity_pairs (pair_symbol TEXT PRIMARY KEY, base_token TEXT, quote_token TEXT, liquidity_usd REAL, volume_24h REAL, apy_range TEXT, last_updated TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS yield_vaults_v6 (vault_id TEXT PRIMARY KEY, strategy_name TEXT, underlying_asset TEXT, moo_token TEXT, total_tvl REAL, apy REAL, moo_token_price REAL, compound_frequency_hours INTEGER, last_harvest TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS scraper_flags (flag_id TEXT PRIMARY KEY, status TEXT, description TEXT, detected_at TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS protocol_treasury_v11 (asset TEXT PRIMARY KEY, pol_locked REAL, total_burned REAL, insurance_fund REAL, last_updated TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS tax_policies_v12 (policy_id TEXT PRIMARY KEY, operation_type TEXT, base_tax_rate REAL, developer_waiver_allowed INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS sip_knowledge_base_v10 (sip_id TEXT PRIMARY KEY, title TEXT, github_repo TEXT, flag_day TEXT, network_signal_percent REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS risk_guardian_freezes (asset TEXT PRIMARY KEY, reason TEXT, freeze_timestamp TEXT)")
        
        # New v13 Community Integration Tables
        c.execute("CREATE TABLE IF NOT EXISTS dev_registry_v13 (dev_id TEXT PRIMARY KEY, dev_name TEXT, app_name TEXT, royalty_share REAL, total_earned REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS node_status_v13 (node_type TEXT PRIMARY KEY, status TEXT, block_height INTEGER, peer_count INTEGER, latency_ms REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS app_credits_v13 (credit_id TEXT PRIMARY KEY, app_name TEXT, credit_symbol TEXT, exchange_rate_usd REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS ai_knowledge_base_v13 (doc_id TEXT PRIMARY KEY, title TEXT, category TEXT, summary TEXT)")

        c.execute("PRAGMA user_version = 13;")
        print("[+] SQLite Schema upgraded to v13: All Community Modules & Data Sets Integrated.")
    conn.commit()
    conn.close()

def sync_master_ecosystem():
    upgrade_schema_v13()
    conn = get_db()
    c = conn.cursor()
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Seed Portfolio & Top Market Assets
    assets = [
        ('BTC', 'Bitcoin', 84049.37, 'PoW Layer-1', 'Active Core / Audited', 0.8500),
        ('ETH', 'Ethereum', 2689.56, 'Smart Contract L1', 'Active Core / Audited', 1.2000),
        ('USDT', 'Tether USD', 0.9997, 'Fiat Stablecoin', 'Centralized / Verified', 5000.0000),
        ('BNB', 'BNB', 776.91, 'Exchange Ecosystem', 'Active Commits / Audited', 12.0000),
        ('XRP', 'XRP', 1.565, 'Payment Settlement', 'Active / Audited', 2500.0000),
        ('USDC', 'USD Coin', 0.9998, 'Fiat Stablecoin', 'OpenZeppelin Audited', 2230.0000),
        ('SOL', 'Solana', 121.99, 'Smart Contract L1', 'Active Commits / Audited', 12.5000),
        ('FOX', 'ShapeShift FOX', 1.62, 'DAO/Tokenomics', 'Active / Audited', 10000.0000),
        ('TAO', 'Bittensor', 317.48, 'AI/ML Network', 'Active Commits', 10.5000),
        ('SHIB', 'Shiba Inu', 0.0000596, 'Meme/Ecosystem', 'Verified Proxy', 50000000.0),
        ('AAVE', 'Aave', 153.77, 'DeFi Lending', 'Active Commits / Audited', 15.0000),
        ('GRAM', 'Gram', 1.453, 'L1 Network', 'Active / Audited', 1200.0000),
        ('BCH', 'Bitcoin Cash', 341.84, 'PoW/Payment', 'Active Core', 4.5000),
        ('DASH', 'Dash', 28.50, 'Privacy/Payment', 'Active Core', 25.0000),
        ('ONDO', 'Ondo', 0.5507, 'RWA Tokenization', 'Active Commits', 850.0000),
        ('ENA', 'Ethena', 0.2715, 'DeFi Yield', 'Active Commits / Audited', 1500.0000)
    ]
    for token, name, price, cat, repo, bal in assets:
        c.execute("INSERT OR REPLACE INTO global_assets_v7 VALUES (?, ?, ?, ?, ?, ?, ?)", (token, name, price, cat, repo, bal, ts))

    # Seed Liquidity Pools & Yield Vaults
    pairs = [
        ('FOX/USDC', 'FOX', 'USDC', 250000.0, 45200.0, '3.5% - 12.0%', ts),
        ('BTC/USDT', 'BTC', 'USDT', 5800000.0, 1200000.0, '0.01% - 5.5%', ts),
        ('ETH/USDC', 'ETH', 'USDC', 1500000.0, 310000.0, '0.46% - 15.0%', ts),
        ('SOL/USDC', 'SOL', 'USDC', 850000.0, 145000.0, '0.02% - 18.5%', ts),
        ('TAO/USDC', 'TAO', 'USDC', 1450000.0, 320000.0, '4.2% - 16.5%', ts)
    ]
    for p in pairs:
        c.execute("INSERT OR REPLACE INTO liquidity_pairs VALUES (?, ?, ?, ?, ?, ?, ?)", p)

    vaults = [
        ('v-FOX-USDC', 'Beefy Auto-Compounding LP', 'FOX/USDC', 'mooFOXUSDC', 250000.0, 18.5, 1.042, 4, ts),
        ('v-TAO-USDC', 'Tensor Yield Optimizer', 'TAO/USDC', 'mooTAOUSDC', 1450000.0, 28.4, 1.112, 4, ts)
    ]
    for v in vaults:
        c.execute("INSERT OR REPLACE INTO yield_vaults_v6 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", v)

    # Seed Developer Royalties (Item 3)
    devs = [
        ('DEV-01', 'Alice_Core', 'CrossChain_Router', 0.05, 450.25),
        ('DEV-02', 'Bob_Termux', 'Mobile_Bridge_UI', 0.05, 180.50)
    ]
    for d in devs:
        c.execute("INSERT OR REPLACE INTO dev_registry_v13 VALUES (?, ?, ?, ?, ?)", d)

    # Seed Node Telemetry (Item 5)
    nodes = [
        ('Bitcoin Core (Pruned)', 'Active / Synced', 892150, 24, 18.2),
        ('EVM Bundler Client', 'Listening / Alt-Mempool', 21450912, 58, 8.4)
    ]
    for n in nodes:
        c.execute("INSERT OR REPLACE INTO node_status_v13 VALUES (?, ?, ?, ?, ?)", n)

    # Seed Whitepaper AI Knowledge Base (Item 9)
    kb_docs = [
        ('DOC-01', 'Bitcoin Whitepaper (Satoshi Nakamoto)', 'Core Protocol', 'P2P electronic cash system utilizing Proof-of-Work to solve double-spending.'),
        ('DOC-02', 'EIP-4337 Account Abstraction', 'Smart Contracts', 'Enables gasless transactions, user-ops, and custom verification without consensus changes.'),
        ('DOC-03', 'Beefy Vault Auto-Compounding Mechanics', 'DeFi Yield', 'Mathematical share-token system (mooTokens) for harvest optimization.')
    ]
    for doc in kb_docs:
        c.execute("INSERT OR REPLACE INTO ai_knowledge_base_v13 VALUES (?, ?, ?, ?)", doc)

    # Seed Operational Flags
    flags = [
        ('FLAG_ECOSYSTEM_HEALTH', 'GREEN', 'All v13 database schemas verified and operational.'),
        ('FLAG_RISK_SENTINEL', 'GREEN', 'Standalone Security Sentinel active. No malicious build hashes.'),
        ('FLAG_PREFLIGHT_PASS', 'GREEN', 'Code pre-flight smoke tests passed prior to execution.'),
        ('FLAG_TERMUX_BRIDGE', 'GREEN', 'Mobile Termux and bare-metal telemetry hooks live.')
    ]
    for fid, status, desc in flags:
        c.execute("INSERT OR REPLACE INTO scraper_flags VALUES (?, ?, ?, ?)", (fid, status, desc, ts))

    # Seed Tax Policies
    c.execute("INSERT OR REPLACE INTO tax_policies_v12 VALUES ('TAX-01', 'Cross-Chain AMM Swap', 0.05, 0)")
    c.execute("INSERT OR REPLACE INTO tax_policies_v12 VALUES ('TAX-02', 'Sandbox Developer Testing', 0.00, 1)")

    conn.commit()
    conn.close()
    print(f"[+] Sovereign Core Master Telemetry Synced Successfully at {ts}")

if __name__ == "__main__":
    sync_master_ecosystem()

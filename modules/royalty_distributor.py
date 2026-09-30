import sqlite3
import os

PLUGIN_NAME = "RoyaltyConsensus"
VERSION = "1.1.0"

def calculate_consensus_yields():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/wallet.db")
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ecosystem_treasury (
                treasury_id TEXT PRIMARY KEY,
                liquidity_pool_allocation REAL,
                miner_reward_pool REAL
            )
        """)
        conn.execute("INSERT OR IGNORE INTO ecosystem_treasury (treasury_id, liquidity_pool_allocation, miner_reward_pool) VALUES ('global_v1', 0.0, 0.0)")
        
        c = conn.cursor()
        c.execute("SELECT SUM(earnings_usd) FROM earnings_portfolio")
        total_raw = c.fetchone()[0] or 0.0
        
        ecosystem_tax = round(total_raw * 0.05, 4)
        net_yield = round(total_raw * 0.95, 4)
        
        emulated_dex_volume = 10000.00
        miner_fee = round(emulated_dex_volume * 0.0005, 4)
        
        conn.execute("UPDATE ecosystem_treasury SET liquidity_pool_allocation = ?, miner_reward_pool = ? WHERE treasury_id = 'global_v1'", (ecosystem_tax, miner_fee))
        conn.commit()
        conn.close()
        
        return {
            "gross_yield": total_raw,
            "net_node_yield": net_yield,
            "ecosystem_tax_5pct": ecosystem_tax,
            "miner_rewards_0_05pct": miner_fee
        }
    except Exception as e:
        return {"gross_yield": 0.0, "net_node_yield": 0.0, "ecosystem_tax_5pct": 0.0, "miner_rewards_0_05pct": 0.0, "error": str(e)}

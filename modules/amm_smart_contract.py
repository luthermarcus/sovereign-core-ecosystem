# Sovereign Core Production Plugin: Off-Chain AMM & Auto-Compounder (Self-Healing Schema)
import sqlite3
import os

PLUGIN_NAME = "AMMSmartContract"
VERSION = "1.1.0"

def execute_amm_compounding():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/wallet.db")
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        
        # Ensure dex_reserves table has all required columns safely
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dex_reserves (
                token_pair TEXT PRIMARY KEY,
                base_reserve REAL,
                virtual_reserve REAL,
                exchange_rate REAL
            )
        """)
        
        # Self-healing check: Ensure columns exist if table was created older
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(dex_reserves)")
        columns = [col[1] for col in cursor.fetchall()]
        if "base_reserve" not in columns:
            conn.execute("ALTER TABLE dex_reserves ADD COLUMN base_reserve REAL DEFAULT 1000.0")
        if "virtual_reserve" not in columns:
            conn.execute("ALTER TABLE dex_reserves ADD COLUMN virtual_reserve REAL DEFAULT 50000.0")

        # Initialize default pools if empty
        conn.execute("INSERT OR IGNORE INTO dex_reserves (token_pair, base_reserve, virtual_reserve, exchange_rate) VALUES ('FOX/BTC', 1000.0, 50000.0, 0.02)")
        conn.execute("INSERT OR IGNORE INTO dex_reserves (token_pair, base_reserve, virtual_reserve, exchange_rate) VALUES ('PARROT/BTC', 1000.0, 100000.0, 0.01)")
        
        # Fetch the current Liquidity Treasury (The 5% SC-GPL Tax)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ecosystem_treasury (
                treasury_id TEXT PRIMARY KEY,
                liquidity_pool_allocation REAL,
                miner_reward_pool REAL
            )
        """)
        conn.execute("INSERT OR IGNORE INTO ecosystem_treasury (treasury_id, liquidity_pool_allocation, miner_reward_pool) VALUES ('global_v1', 0.0, 0.0)")
        
        c = conn.cursor()
        c.execute("SELECT liquidity_pool_allocation FROM ecosystem_treasury WHERE treasury_id = 'global_v1'")
        treasury_row = c.fetchone()
        treasury_yield = treasury_row[0] if treasury_row else 0.0
        
        if treasury_yield > 0:
            compound_split = treasury_yield / 2
            c.execute("SELECT token_pair, base_reserve, virtual_reserve FROM dex_reserves")
            pools = c.fetchall()
            for pool in pools:
                pair, base, virt = pool
                new_base = base + compound_split
                new_rate = round(new_base / virt, 6) if virt > 0 else 0.0
                conn.execute("UPDATE dex_reserves SET base_reserve = ?, exchange_rate = ? WHERE token_pair = ?", (new_base, new_rate, pair))
                
            conn.execute("UPDATE ecosystem_treasury SET liquidity_pool_allocation = 0.0 WHERE treasury_id = 'global_v1'")
            
        conn.commit()
        conn.close()
        return f"Status: Active (AMM Auto-Compounded Yield into DEX Pools)"
    except Exception as e:
        return f"Status: AMM Error ({e})"

if __name__ == "__main__":
    print(execute_amm_compounding())

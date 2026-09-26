import sqlite3
import datetime

DB_PATH = "/home/luther/sovereign-core-ecosystem/wallet.db"

def init_wallet():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS wallet_state (
            address TEXT PRIMARY KEY,
            balance REAL,
            staked_power REAL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS innovations (
            id TEXT PRIMARY KEY,
            module_name TEXT,
            author TEXT,
            royalty_rate REAL,
            earnings REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Initialize default master wallet if empty
    conn.execute("REPLACE INTO wallet_state (address, balance, staked_power) VALUES (?, ?, ?)", 
                 ("sovereign1luther_master_node_x79", 142.50, 85.0))
    # Initialize default innovation copyright stake (5% model)
    conn.execute("REPLACE INTO innovations (id, module_name, author, royalty_rate, earnings) VALUES (?, ?, ?, ?, ?)",
                 ("inv_001", "Sovereign Core Microkernel", "Luther M.", 0.05, 12.45))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_wallet()
    print("[+] Innovation Royalty & Wallet Ledger initialized.")

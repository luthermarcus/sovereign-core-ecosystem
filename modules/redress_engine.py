import os, sys, time, sqlite3
sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class WalletRedressEngine:
    DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")

    @classmethod
    def setup_redress_tables(cls):
        conn = sqlite3.connect(cls.DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wallet_reputation (
                wallet_address TEXT PRIMARY KEY,
                reputation_status TEXT DEFAULT 'PROBATION',
                risk_score REAL DEFAULT 75.0,
                escrow_balance REAL DEFAULT 0.0,
                updated_at REAL
            )
        """)
        conn.commit()
        conn.close()

    @classmethod
    def flag_bad_actor(cls, wallet_address, disputed_amount):
        cls.setup_redress_tables()
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO wallet_reputation (wallet_address, reputation_status, risk_score, escrow_balance, updated_at)
            VALUES (?, 'PROBATION', 90.0, ?, ?)
            ON CONFLICT(wallet_address) DO UPDATE SET
                reputation_status='PROBATION',
                risk_score=90.0,
                escrow_balance=escrow_balance + ?,
                updated_at=?
        """, (wallet_address, disputed_amount, time.time(), disputed_amount, time.time()))
        conn.commit()
        conn.close()
        print(f"\n[!] [REDRESS ENGINE] Wallet {wallet_address} flagged. Placed on PROBATION. Escrow locked: {disputed_amount} coins.")

    @classmethod
    def rectify_and_refund(cls, wallet_address):
        cls.setup_redress_tables()
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT escrow_balance FROM wallet_reputation WHERE wallet_address = ?", (wallet_address,))
        row = cursor.fetchone()
        
        if not row or row[0] <= 0:
            print(f"\n[-] [REDRESS ENGINE] No active escrow or funds found for {wallet_address}.")
            conn.close()
            return False

        cursor.execute("""
            UPDATE wallet_reputation 
            SET reputation_status = 'REHABILITATED', risk_score = 10.0, escrow_balance = 0.0, updated_at = ?
            WHERE wallet_address = ?
        """, (time.time(), wallet_address))
        conn.commit()
        conn.close()
        print(f"\n[v] [REDRESS ENGINE] Wallet {wallet_address} successfully rectified wrongs! Status updated to REHABILITATED.")
        return True

if __name__ == "__main__":
    test_wallet = "node_peer_alpha_99"
    print("=== INITIATING REDRESS & REPUTATION WORKFLOW ===")
    WalletRedressEngine.flag_bad_actor(test_wallet, 0.50)
    WalletRedressEngine.rectify_and_refund(test_wallet)

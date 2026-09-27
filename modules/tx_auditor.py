import sqlite3, os, time

class TransactionAuditor:
    DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/wallet.db")

    @classmethod
    def setup_ledgers(cls):
        conn = sqlite3.connect(cls.DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("CREATE TABLE IF NOT EXISTS balances (account TEXT PRIMARY KEY, amount REAL)")
        conn.execute("CREATE TABLE IF NOT EXISTS audit_ledger (tx_id TEXT, amount REAL, reason TEXT, timestamp REAL)")
        conn.execute("INSERT OR IGNORE INTO balances (account, amount) VALUES ('L1_MAIN', 1.25)")
        conn.commit()
        conn.close()

    @classmethod
    def execute_safeguarded_transaction(cls, tx_id, amount, flag_for_audit=False):
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        try:
            # 1. Open Mathematical State
            conn.execute("BEGIN TRANSACTION")
            
            # 2. Attempt Deduction
            cursor.execute("UPDATE balances SET amount = amount - ? WHERE account = 'L1_MAIN'", (amount,))
            
            # 3. Security Warden Check
            if flag_for_audit:
                # Log to the audit ledger for review
                cursor.execute("INSERT INTO audit_ledger (tx_id, amount, reason, timestamp) VALUES (?, ?, ?, ?)", 
                               (tx_id, amount, "FAILED_SECURITY_SIGNATURE", time.time()))
                # Trigger Mathematical Rollback
                conn.execute("ROLLBACK")
                print(f"[!] Warden Alert: TX {tx_id} flagged. State ROLLED BACK. Funds secured.")
            else:
                conn.execute("COMMIT")
                print(f"[v] TX {tx_id} cleared and committed.")
                
        except Exception as e:
            conn.execute("ROLLBACK")
            print(f"[-] System Error. State Rolled Back: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    TransactionAuditor.setup_ledgers()
    print("=== INITIATING SAFEGUARDED TRANSACTION ===")
    TransactionAuditor.execute_safeguarded_transaction("TX_9988_SUSPICIOUS", 0.15, flag_for_audit=True)

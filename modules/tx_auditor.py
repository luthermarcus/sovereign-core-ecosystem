import sqlite3, os, time
from modules.zero_trust_mediator import ZeroTrustMediator

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
        # PROACTIVE SECURITY: Route through the Zero-Trust Mediator FIRST
        if not ZeroTrustMediator.simulate_connection(tx_id, amount):
            # The mediator killed the connection before it ever reached the database.
            return

        print("\n[*] [L1/L2 PIPELINE] Processing verified transaction...")
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        try:
            conn.execute("BEGIN TRANSACTION")
            cursor.execute("UPDATE balances SET amount = amount - ? WHERE account = 'L1_MAIN'", (amount,))
            
            if flag_for_audit:
                conn.execute("ROLLBACK")
                print(f"[!] [AUDITOR] Llate-stage anomaly detected. State ROLLED BACK. Funds secured.")
                conn.execute("BEGIN TRANSACTION")
                cursor.execute("INSERT INTO audit_ledger (tx_id, amount, reason, timestamp) VALUES (?, ?, ?, ?)", 
                               (tx_id, amount, "FAILED_LATE_STAGE_SIGNATURE", time.time()))
                conn.commit()
            else:
                conn.commit()
                print(f"[v] [AUDITOR] TX {tx_id} safely cleared and committed to L1 Anchor.")
                
        except Exception as e:
            conn.execute("ROLLBACK")
            print(f"[-] [AUDITOR] System Error. State Rolled Back: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    TransactionAuditor.setup_ledgers()
    print("=== INITIATING ZERO-TRUST MEDIATOR TESTS ===")
    
    # Test 1: Malicious Connection (Should be dropped proactively by the Mediator)
    TransactionAuditor.execute_safeguarded_transaction("TX_8888_MALICIOUS", 0.75)
    
    # Test 2: Clean Connection (Should pass Mediator and be processed by the Auditor)
    TransactionAuditor.execute_safeguarded_transaction("TX_9999_CLEAN_DEPIN_YIELD", 0.15)

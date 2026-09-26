import time
import hashlib
import json

class TransactionGuard:
    CHALLENGE_WINDOW_SEC = 5.0  # Optimistic challenge period for testing

    @staticmethod
    def submit_provisional_transaction(tx_id, sender, amount, is_malicious=False):
        """Stages a transaction in provisional escrow for challenge evaluation."""
        tx_packet = {
            "tx_id": tx_id,
            "sender": sender,
            "amount": amount,
            "status": "PENDING_CHALLENGE_PERIOD",
            "timestamp": time.time(),
            "malicious_flag": is_malicious
        }
        return tx_packet

    @classmethod
    def evaluate_challenge_window(cls, tx_packet):
        """Evaluates fraud proofs during the challenge window to execute recalls if necessary."""
        time.sleep(0.5) # Simulate challenge validation check
        
        if tx_packet["malicious_flag"]:
            return {
                "tx_id": tx_packet["tx_id"],
                "status": "RECALLED_AND_REVERTED",
                "reason": "Fraud Proof Verified: Malicious transaction pattern detected.",
                "penalty": "100% Stake Slashing Triggered"
            }
        else:
            return {
                "tx_id": tx_packet["tx_id"],
                "status": "FINALIZED_AND_ANCHORED",
                "reason": "Challenge window expired with zero fraud proofs.",
                "penalty": "None (Nominal Execution)"
            }

#!/usr/bin/env python3
import hashlib
import json
import os
import time

SANDBOX_LEDGER = "/root/workspace/bitcoin_sandbox.json"

def sha256d(data: bytes) -> str:
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

def init_sandbox():
    if not os.path.exists(SANDBOX_LEDGER) or os.path.getsize(SANDBOX_LEDGER) == 0:
        os.makedirs(os.path.dirname(SANDBOX_LEDGER), exist_ok=True)
        initial_state = {
            "chain": "regtest",
            "block_height": 101,
            "utxos": [
                {"txid": sha256d(b"genesis_coinbase"), "vout": 0, "amount_sats": 5000000000, "status": "confirmed"}
            ],
            "channel_vaults": [],
            "last_audit": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(SANDBOX_LEDGER, "w") as f:
            json.dump(initial_state, f, indent=2)

def simulate_channel_settlement():
    init_sandbox()
    with open(SANDBOX_LEDGER, "r") as f:
        state = json.load(f)

    state["block_height"] += 1
    new_channel = {
        "channel_id": sha256d(f"channel_{state['block_height']}_{time.time()}".encode())[:16],
        "capacity_sats": 1000000,
        "local_balance": 750000,
        "remote_balance": 250000,
        "settlement_state": "VERIFIED_ISOLATED"
    }
    state["channel_vaults"].append(new_channel)
    state["last_audit"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(SANDBOX_LEDGER, "w") as f:
        json.dump(state, f, indent=2)

    print(f"[+] Bitcoin Sandbox Block #{state['block_height']}: Channel {new_channel['channel_id']} committed.")
    print(f"    Local Balance: {new_channel['local_balance']} sats | Remote Balance: {new_channel['remote_balance']} sats")
    print(f"    State Settlement: {new_channel['settlement_state']}")

if __name__ == "__main__":
    simulate_channel_settlement()

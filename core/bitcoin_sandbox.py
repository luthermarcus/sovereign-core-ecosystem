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
            "block_height": 102,
            "multisig_vaults": [],
            "last_audit": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(SANDBOX_LEDGER, "w") as f:
            json.dump(initial_state, f, indent=2)

def simulate_channel_settlement():
    init_sandbox()
    with open(SANDBOX_LEDGER, "r") as f:
        state = json.load(f)

    state["block_height"] += 1
    channel_seed = f"multisig_channel_{state['block_height']}_{time.time()}"
    channel_id = sha256d(channel_seed.encode())[:16]
    preimage = os.urandom(32).hex()
    payment_hash = hashlib.sha256(bytes.fromhex(preimage)).hexdigest()

    new_channel = {
        "channel_id": channel_id,
        "funding_type": "2-of-2_MULTISIG",
        "capacity_sats": 2000000,
        "local_balance": 1400000,
        "remote_balance": 600000,
        "htlc": {
            "payment_hash": payment_hash[:16],
            "amount_sats": 100000,
            "timelock_blocks": state["block_height"] + 144,
            "status": "SETTLED_OFFCHAIN"
        },
        "settlement_state": "VERIFIED_ISOLATED"
    }
    
    if "multisig_vaults" not in state:
        state["multisig_vaults"] = []
    state["multisig_vaults"].append(new_channel)
    state["last_audit"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(SANDBOX_LEDGER, "w") as f:
        json.dump(state, f, indent=2)

    print(f"[+] Bitcoin L2 Block #{state['block_height']}: 2-of-2 Channel {channel_id} settled.")
    print(f"    Capacity: {new_channel['capacity_sats']} sats | Local: {new_channel['local_balance']} | Remote: {new_channel['remote_balance']}")
    print(f"    HTLC Hash: {payment_hash[:16]}... | Timelock: +144 Blocks | State: {new_channel['settlement_state']}")

if __name__ == "__main__":
    simulate_channel_settlement()

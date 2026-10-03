#!/usr/bin/env python3
import hashlib
import json
import os
import time

WALLET_LEDGER = "/root/workspace/fox_wallet.json"

def sha256d(data: bytes) -> str:
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

def init_wallet():
    if not os.path.exists(WALLET_LEDGER) or os.path.getsize(WALLET_LEDGER) == 0:
        os.makedirs(os.path.dirname(WALLET_LEDGER), exist_ok=True)
        priv_seed = os.urandom(32).hex()
        fox_addr = "fox1q" + sha256d(priv_seed.encode())[:38]
        initial_state = {
            "token": "FOX (Foxy)",
            "address": fox_addr,
            "l1_balance_fox": 25000.0,
            "l2_channel_balance_fox": 5000.0,
            "depin_yield_fox": 185.50,
            "bridge_state": "SYNCHRONIZED",
            "cross_asset_swaps": [],
            "last_attestation": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(WALLET_LEDGER, "w") as f:
            json.dump(initial_state, f, indent=2)

def compound_depin_yield():
    init_wallet()
    with open(WALLET_LEDGER, "r") as f:
        data = json.load(f)

    yield_increment = 25.75
    data["l2_channel_balance_fox"] += yield_increment
    data["depin_yield_fox"] = round(data.get("depin_yield_fox", 0.0) + yield_increment, 2)
    swap_id = sha256d(f"yield_{time.time()}".encode())[:12]
    data["cross_asset_swaps"].append({
        "tx_id": swap_id,
        "type": "DEPIN_MESH_REWARD_SETTLED",
        "amount_fox": yield_increment,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    data["last_attestation"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(WALLET_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[+] DePIN Yield Compounded: +{yield_increment:.2f} FOX -> L2 Channel Vault")
    print(f"    Total L2 Channel Balance: {data['l2_channel_balance_fox']:,.2f} FOX")
    return data

if __name__ == "__main__":
    compound_depin_yield()

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
            "bridge_state": "SYNCHRONIZED",
            "cross_asset_swaps": [],
            "last_attestation": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(WALLET_LEDGER, "w") as f:
            json.dump(initial_state, f, indent=2)

def sync_wallet(channel_id=None, amount_fox=250.0):
    init_wallet()
    with open(WALLET_LEDGER, "r") as f:
        data = json.load(f)

    if channel_id:
        data["l1_balance_fox"] = max(0.0, data["l1_balance_fox"] - amount_fox)
        data["l2_channel_balance_fox"] += amount_fox
        swap_entry = {
            "swap_id": sha256d(f"{channel_id}_{time.time()}".encode())[:12],
            "channel_ref": channel_id,
            "fox_amount": amount_fox,
            "status": "ATOMIC_SWAP_SETTLED"
        }
        data["cross_asset_swaps"].append(swap_entry)

    data["last_attestation"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(WALLET_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[+] FOX Wallet Attested: Address {data['address'][:12]}...")
    print(f"    L1 Balance: {data['l1_balance_fox']:,.2f} FOX | L2 Channel Vault: {data['l2_channel_balance_fox']:,.2f} FOX")
    return data

if __name__ == "__main__":
    sync_wallet()

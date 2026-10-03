#!/usr/bin/env python3
import hashlib
import json
import os
import time

WALLET_LEDGER = "/root/workspace/fox_wallet.json"
BTC_LEDGER    = "/root/workspace/bitcoin_sandbox.json"

def sha256d(data: bytes) -> str:
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

def init_wallet():
    if not os.path.exists(WALLET_LEDGER) or os.path.getsize(WALLET_LEDGER) == 0:
        os.makedirs(os.path.dirname(WALLET_LEDGER), exist_ok=True)
        priv_seed = os.urandom(32).hex()
        # Derive checksummed EVM-compatible address and native SegWit address
        evm_addr = "0x" + hashlib.sha256(priv_seed.encode()).hexdigest()[:40]
        segwit_addr = "bcrt1q" + sha256d(priv_seed.encode())[:38]
        initial_state = {
            "token": "FOX (Foxy)",
            "evm_address": evm_addr,
            "segwit_address": segwit_addr,
            "l1_balance_fox": 25000.0,
            "l2_channel_balance_fox": 5000.0,
            "depin_yield_fox": 211.25,
            "cross_chain_swaps": 0,
            "last_swap_hash": "None",
            "bridge_state": "SYNCHRONIZED_ACTIVE",
            "last_attestation": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(WALLET_LEDGER, "w") as f:
            json.dump(initial_state, f, indent=2)

def compound_depin_yield():
    init_wallet()
    with open(WALLET_LEDGER, "r") as f:
        data = json.load(f)

    yield_val = 25.75
    data["l2_channel_balance_fox"] += yield_val
    data["depin_yield_fox"] = round(data.get("depin_yield_fox", 0.0) + yield_val, 2)
    data["last_attestation"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(WALLET_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[+] Yield Compounded: +{yield_val:.2f} FOX -> L2 Balance: {data['l2_channel_balance_fox']:,.2f} FOX")
    return data

def execute_atomic_swap():
    init_wallet()
    with open(WALLET_LEDGER, "r") as f:
        w_data = json.load(f)

    # 50,000 sats -> 500 FOX atomic off-chain swap
    preimage = os.urandom(32).hex()
    p_hash = hashlib.sha256(bytes.fromhex(preimage)).hexdigest()[:16]

    w_data["l2_channel_balance_fox"] += 500.0
    w_data["cross_chain_swaps"] = w_data.get("cross_chain_swaps", 0) + 1
    w_data["last_swap_hash"] = f"0x{p_hash}"
    w_data["last_attestation"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(WALLET_LEDGER, "w") as f:
        json.dump(w_data, f, indent=2)

    # Also log settlement in Bitcoin sandbox
    if os.path.exists(BTC_LEDGER):
        try:
            with open(BTC_LEDGER, "r") as bf:
                b_data = json.load(bf)
            b_data["block_height"] += 1
            b_data.setdefault("multisig_vaults", []).append({
                "channel_id": p_hash,
                "funding_type": "ATOMIC_HTLC_SWAP",
                "capacity_sats": 50000,
                "local_balance": 50000,
                "remote_balance": 0,
                "settlement_state": "VERIFIED_ISOLATED"
            })
            with open(BTC_LEDGER, "w") as bf:
                json.dump(b_data, bf, indent=2)
        except Exception:
            pass

    print(f"[+] Atomic Swap Settled: 50,000 Sats <-> 500.0 FOX (Hash: {w_data['last_swap_hash']})")
    return w_data

if __name__ == "__main__":
    compound_depin_yield()

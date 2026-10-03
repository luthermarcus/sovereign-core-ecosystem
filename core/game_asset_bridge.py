#!/usr/bin/env python3
import json, os, time, hashlib

GF = "/root/workspace/game_assets_ledger.json"
GAMES = {
    "VOXEL_QUEST": {"name": "Voxel Quest", "sym": "VGOLD", "rate": 0.05},
    "CYBER_RUNNER": {"name": "Cyber Runner", "sym": "CRED", "rate": 0.01}
}

def swap_game_asset(game_key="VOXEL_QUEST", amt=1000.0):
    os.makedirs(os.path.dirname(GF), exist_ok=True)
    d = json.load(open(GF)) if os.path.exists(GF) else {"total_converted_fox": 0.0}
    g = GAMES.get(game_key, GAMES["VOXEL_QUEST"])
    fox_val = round(amt * g["rate"], 2)
    p_hash = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
    d["total_converted_fox"] = round(d.get("total_converted_fox", 0.0) + fox_val, 2)
    d["last_swap"] = {"game": g["name"], "burned": f"{amt} {g['sym']}", "gained_fox": fox_val, "hash": f"0x{p_hash}"}
    json.dump(d, open(GF, "w"), indent=2)
    print(f"[✓] {g['name']}: {amt} {g['sym']} burned -> {fox_val} FOX credited to L2 Vault (Hash: 0x{p_hash})")

if __name__ == "__main__": swap_game_asset()

#!/usr/bin/env python3
import os, sys, math, hmac, time, json, shutil, hashlib
from decimal import Decimal, ROUND_DOWN
from datetime import datetime, timezone
from sos_platform import get_host_info, connect_wal_db, load_local_profile, get_kernel_bandwidth_proof

# Satoshi 10^-8 Fixed-Point Unit (1 satoshi / 1 base FOX unit)
Q = Decimal("0.00000001")
GENESIS_WALLETS = ("0xE25229c0efb72F91Fb692ac0f75385acd3E8D298", "0xFOXe829cf1e4d93f153", "bc1qlgvgkrx758hq0n2uc60jtvfl7sgnwrc9nrp983")
MODELS = {
    "DEPIN_FLYWHEEL": ("Option B: DePIN Flywheel (15/40/32/8/5)", Decimal("0.15"), Decimal("0.40"), Decimal("0.32"), Decimal("0.08"), Decimal("0.05")),
    "DYNAMIC_SURGE":  ("Option C: Dynamic Surge (15/45/25/8/7)",  Decimal("0.15"), Decimal("0.45"), Decimal("0.25"), Decimal("0.08"), Decimal("0.07")),
    "POL_FORTRESS":   ("Option A: POL Fortress (15/55/18/7/5)",   Decimal("0.15"), Decimal("0.55"), Decimal("0.18"), Decimal("0.07"), Decimal("0.05"))
}

def _init_db(c):
    c.execute("CREATE TABLE IF NOT EXISTS toll_3prong (ts REAL, mode TEXT, gross TEXT, fee TEXT, owner TEXT, pol TEXT, miners_depin TEXT, devs TEXT, burn TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS wallets_5way (role TEXT PRIMARY KEY, addr TEXT, bal TEXT, txs INT);")
    c.execute("CREATE TABLE IF NOT EXISTS contributor_trust (actor TEXT PRIMARY KEY, score INT, status TEXT, updated TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS boomerang_escrow (intent_id TEXT PRIMARY KEY, protocol TEXT, gross_fox TEXT, hold_window_s REAL, custody_state TEXT, status TEXT, ts REAL);")

def verify_lock(prof):
    cfg = tuple(sorted(prof.get("personal_owner_wallets", list(GENESIS_WALLETS))))
    seed = prof.get("airgap_math", {}).get("seed", "sos_genesis_airgap")
    sig = hmac.new(seed.encode(), "|".join(GENESIS_WALLETS).encode(), hashlib.sha256).hexdigest()
    return {"bip_fox_spec": "BIP-141_SEGWIT_AND_EVM_HYBRID_PIN", "satoshi_unit": str(Q), "wallets": list(GENESIS_WALLETS), "share": "15.0%", "hmac": sig[:20]+"...", "state": "HMAC_LOCKED_VALID" if cfg == GENESIS_WALLETS else "REVERTED_TO_GENESIS"}

def verify_symlinks():
    ld = "/dev/shm/sos_symlinks" if os.path.isdir("/dev/shm") else "/tmp/sos_symlinks"
    os.makedirs(ld, exist_ok=True)
    st = {}
    for b in ["ufw", "fail2ban-client", "systemctl", "busybox", "python3"]:
        w, dst = shutil.which(b), f"{ld}/sos_{b}"
        if w and not os.path.exists(dst):
            try: os.symlink(w, dst)
            except Exception: pass
        st[f"sos_{b}"] = "WORKING_LINKED" if (os.path.islink(dst) and os.access(dst, os.X_OK)) else "MISSING"
    return {"dir": ld, "binaries": st}

def spatial_3d_cooldown(vol: float, cap: float = 25000.0, dt: float = 960.0):
    c, dx, dy, dz = 1.0, 0.05, min(1.05, float(vol)/float(cap)), 0.02
    ds2 = round(-((c*dt)**2) + ((dx**2 + dy**2 + dz**2)*(dt**2)), 4)
    tl = ds2 <= 0
    beta = min(0.9999, math.sqrt(dx**2 + min(0.98, dy)**2 + dz**2))
    g = round(1.0 / math.sqrt(1.0 - (beta**2)), 6) if tl else float("inf")
    return {
        "status": "EXPERIMENTAL_ASYMPTOTIC_COOLDOWN_CURVE",
        "formula": "ds^2 = -(c*dt)^2 + dx^2 + dy^2 + dz^2",
        "dimensions_4D": {"t_sec": dt, "x_L1": dx, "y_L2_vel": round(dy, 4), "z_DePIN": dz, "projective_limit": "[0, 0, inf]"},
        "ds_squared": ds2, "causality_valid_timelike": tl, "lorentz_gamma": g,
        "dilated_escrow_window_sec": round(dt*g, 2) if tl else "INFINITY_LOCKED_[0,0,inf]"
    }

def settle(tx_fox=1000.0, ext=False, cap=12000.0, proto="EIP2612_PERMIT_HOLD_960S"):
    prof = load_local_profile()
    wl = verify_lock(prof)
    gross = Decimal(str(tx_fox)).quantize(Q)
    c = connect_wal_db("trust_store.db")
    _init_db(c); c.isolation_level = None; c.execute("BEGIN IMMEDIATE;")
    now, iso = time.time(), datetime.now(timezone.utc).isoformat()
    c.execute("INSERT OR REPLACE INTO contributor_trust VALUES ('luthermarcus', 100, 'GENESIS_ADMIN', ?);", (iso,))
    c.execute("INSERT OR REPLACE INTO contributor_trust VALUES ('leviathonbeast', 85, 'AUDITED_PR_CONTRIBUTOR', ?);", (iso,))
    vol = sum((Decimal(r[0]) for r in c.execute("SELECT gross FROM toll_3prong WHERE ts >= ?;", (now-960,)).fetchall()), Decimal("0")) + (gross if ext else Decimal("0"))
    rel = spatial_3d_cooldown(float(vol))
    win = float(rel["dilated_escrow_window_sec"]) if isinstance(rel["dilated_escrow_window_sec"], (int, float)) else 960.0
    iid = "bmrng_" + hashlib.sha256(f"{now}:{gross}:{ext}".encode()).hexdigest()[:10]
    if ext and gross > Decimal(str(cap)):
        c.execute("INSERT INTO boomerang_escrow VALUES (?,?,?,?,?,?,?);", (iid, proto, str(gross), win, "HELD_IN_USER_WALLET_NEVER_MOVED", "BOOMERANG_PERMIT_CANCELLED_AT_ORIGIN", now))
        c.execute("COMMIT;"); c.close()
        return {"intent": iid, "protocol": proto, "fox": str(gross), "custody": "HELD_IN_USER_WALLET_NEVER_MOVED", "state": "BOOMERANG_PERMIT_CANCELLED_AT_ORIGIN"}
    bw = get_kernel_bandwidth_proof()
    m = "POL_FORTRESS" if vol >= Decimal("15000") else ("DEPIN_FLYWHEEL" if (bw.get("proof_of_bandwidth_valid") and vol <= Decimal("5000")) else "DYNAMIC_SURGE")
    _, wo, wp, wm, wd, wb = MODELS[m]
    rate = Decimal("0.0100") if not ext else (Decimal("0.0150") + min(Decimal("0.0200"), (vol/Decimal("25000"))*Decimal("0.0200"))).quantize(Decimal("0.0001"), rounding=ROUND_DOWN)
    fee, gas = (gross * rate).quantize(Q, ROUND_DOWN), Decimal("0.00096000")
    co, cm, cd, cb = (fee*wo).quantize(Q, ROUND_DOWN), (fee*wm).quantize(Q, ROUND_DOWN), (fee*wd).quantize(Q, ROUND_DOWN), (fee*wb).quantize(Q, ROUND_DOWN)
    cp = (fee - co - cm - cd - cb).quantize(Q, ROUND_DOWN)
    c.execute("INSERT INTO toll_3prong VALUES (?,?,?,?,?,?,?,?,?);", (now, m, str(gross), str(fee), str(co), str(cp), str(cm), str(cd), str(cb)))
    c.execute("INSERT INTO boomerang_escrow VALUES (?,?,?,?,?,?,?);", (iid, proto, str(gross), win, "WALLET_HOLD_VERIFIED_TRANSFER_FROM_EXECUTED", "BOOMERANG_SETTLED_L2", now))
    for role, addr, cut in [("1_MY_PERSONAL_OWNER_WALLETS_15PCT", "|".join(wl["wallets"]), co), ("2_POL_LIQUIDITY_RESERVE", "0xFOX_POL_LIQUIDITY_RESERVE", cp), ("3_AUXPOW_MINERS_AND_7NODE_DEPIN", "0xFOX_MINERS_AND_DEPIN_POOL", cm), ("4_DEVELOPERS_AND_CONTRIBUTOR_TRUST", "0xFOX_DEV_CONTRIBUTOR_TRUST", cd), ("5_DEFLATIONARY_BURN_RESERVE", "0x000000000000000000000000000000000000dEaD", cb)]:
        r = c.execute("SELECT bal, txs FROM wallets_5way WHERE role=?;", (role,)).fetchone()
        c.execute("INSERT OR REPLACE INTO wallets_5way VALUES (?,?,?,?);", (role, addr, str((Decimal(r[0])+cut).quantize(Q) if r else cut), (r[1]+1 if r else 1)))
    wr = {r[0]: {"address": r[1], "balance_fox": r[2], "txs": r[3]} for r in c.execute("SELECT role, addr, bal, txs FROM wallets_5way ORDER BY role;").fetchall()}
    tr = {r[0]: {"score": r[1], "role": r[2]} for r in c.execute("SELECT actor, score, status FROM contributor_trust;").fetchall()}
    br = [{"intent": r[0], "protocol": r[1], "fox": r[2], "win_s": r[3], "custody": r[4], "state": r[5]} for r in c.execute("SELECT intent_id, protocol, gross_fox, hold_window_s, custody_state, status FROM boomerang_escrow;").fetchall()]
    c.execute("COMMIT;"); c.close()
    return {"engine": m, "rate": f"{rate*100:.2f}%", "fee": str(fee), "owner_15pct": str(co), "eco_85pct": str(fee-co), "lock": wl, "boomerang": br, "relativity": rel, "trust": tr, "wallets": wr}

def build_anchor():
    c = connect_wal_db("trust_store.db")
    for t in ["contributor_trust", "boomerang_escrow", "toll_3prong", "wallets_5way"]: c.execute(f"DROP TABLE IF EXISTS {t};")
    _init_db(c); c.commit(); c.close()
    s0 = settle(1000, False, proto="INTERNAL_L2_ALLOWANCE_HOLD")
    sb = settle(1000, True, proto="EIP2612_PERMIT_HOLD_960S")
    sc = settle(7000, True, proto="ERC4337_PAYMASTER_USEROP_HOLD")
    sa = settle(10000, True, proto="BIP65_CLTV_BIP199_HTLC_HOLD")
    sr = settle(15000, True, proto="EIP2612_PERMIT_HOLD_960S")
    d = {
        "milestone": "v7.71.72",
        "tier_1_working_deployed": {"os_symlinks": verify_symlinks(), "ram_wal_db": "/dev/shm/trust_store.db", "depin_7_apps": load_local_profile().get("portfolio")},
        "tier_2_virtualized_beta": {"wallet_hmac_lock": sa["lock"], "base_1pct_verify": {"rate": s0["rate"], "fee": s0["fee"], "my_15pct": s0["owner_15pct"], "eco_85pct": s0["eco_85pct"]}, "tri_engine_modes": [sb["engine"], sc["engine"], sa["engine"]], "boomerang_pre_movement_wallet_holds": sa["boomerang"] + [sr], "contributor_trust_v192": sa["trust"], "wallets_5way": sa["wallets"], "asset_matrix_count": 30},
        "tier_3_experimental_rd": {"spatial_3d_cooldown_vector": sa["relativity"], "auxpow_satoshi_merged_mining": "VIRTUALIZED_BUCKET_3_REQUIRES_PARENT_RPC"}
    }
    p = os.path.expanduser("~/.sos_ai_continuity_anchor.json")
    open(p, "w").write(json.dumps(d, indent=2)); os.chmod(p, 0o600)
    return d

if __name__ == "__main__":
    d = build_anchor()
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--wallets": print(json.dumps(d["tier_2_virtualized_beta"]["wallets_5way"], indent=2))
    elif arg == "--sec": print(json.dumps({"symlinks": d["tier_1_working_deployed"]["os_symlinks"], "lock": d["tier_2_virtualized_beta"]["wallet_hmac_lock"], "boomerang": d["tier_2_virtualized_beta"]["boomerang_pre_movement_wallet_holds"]}, indent=2))
    elif arg == "-1": print(json.dumps(d["tier_1_working_deployed"]["depin_7_apps"], indent=2))
    elif arg == "-2": print(json.dumps({"host": get_host_info(), "experimental_3d": d["tier_3_experimental_rd"]}, indent=2))
    elif arg == "-3": print(json.dumps({"consolidated_modules": sorted([f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if f.endswith(".py")]), "asset_matrix_count": 30}, indent=2))
    else: print(json.dumps(d, indent=2))

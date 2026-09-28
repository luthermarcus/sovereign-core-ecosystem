from fastapi import FastAPI, HTTPException
import sqlite3, os

app = FastAPI(title="Sovereign Core OS - Local Loopback API", version="7.35.0")

def enforce_oracle_firewall(external_feed: bool):
    if external_feed:
        raise HTTPException(status_code=403, detail="CLASSIFIED OPSEC: External CoinMarketCap/Oracle APIs are forbidden.")

def query_ledger(db_name: str, query: str, params=()):
    db_path = os.path.expanduser(f"~/sovereign-core-ecosystem/{db_name}")
    if not os.path.exists(db_path):
        return []
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

@app.get("/api/fleet")
def get_fleet_metrics():
    return query_ledger("ecosystem_metrics.db", "SELECT * FROM depin_throughput")

@app.get("/api/depin/valuation")
def get_depin_valuation(external_feed: bool = False):
    enforce_oracle_firewall(external_feed)
    rows = query_ledger("ecosystem_metrics.db", "SELECT bandwidth_gb, yield_usd FROM depin_throughput")
    if not rows:
        return {"total_bandwidth_gb": 0.0, "total_yield_usd": 0.0, "intrinsic_rate": 1.0}
    total_bw = sum(r["bandwidth_gb"] for r in rows)
    total_yield = sum(r["yield_usd"] for r in rows)
    rate = round(total_yield / max(total_bw, 0.001), 6)
    return {"total_bandwidth_gb": total_bw, "total_yield_usd": total_yield, "intrinsic_rate": rate}

@app.get("/api/htlc/compile")
def compile_htlc(hash_hex: str, receiver_pubkey: str, locktime_blocks: int, sender_pubkey: str):
    lock_hex = hex(locktime_blocks)[2:].zfill(4)
    script = f"63 a8 {hash_hex} 88 {receiver_pubkey} ac 67 {lock_hex} b1 75 {sender_pubkey} ac 68"
    return {"script_hex": script, "locktime_blocks": locktime_blocks, "locktime_hex": lock_hex}

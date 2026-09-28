import os, sqlite3, time, hashlib

def int_to_little_endian_4bytes(val: int) -> str:
    return val.to_bytes(4, byteorder="little", signed=False).hex()

def enforce_cltv_freeze(locktime_blocks: int, pubkey_hex: str):
    lock_le = int_to_little_endian_4bytes(locktime_blocks)
    return f"04 {lock_le} b1 75 21 {pubkey_hex} ac"

def enforce_htlc_swap(hash_hex: str, receiver_pubkey: str, locktime_blocks: int, sender_pubkey: str):
    lock_le = int_to_little_endian_4bytes(locktime_blocks)
    # BIP 199 compliant serialization: OP_IF OP_SHA256 PUSH32 <hash> OP_EQUALVERIFY PUSH33 <rec_pk> OP_CHECKSIG OP_ELSE PUSH4 <lock_le> OP_CLTV OP_DROP PUSH33 <send_pk> OP_CHECKSIG OP_ENDIF
    return f"63 a8 20 {hash_hex} 88 21 {receiver_pubkey} ac 67 04 {lock_le} b1 75 21 {sender_pubkey} ac 68"

def execute_dex_intent_in_ram(intent_data: str):
    shm_path = "/dev/shm/dex_intent_ring.tmp"
    with open(shm_path, "a") as f:
        f.write(intent_data + chr(10))
    return "L2_ROUTED"

def sync_depin_yields_with_hashchain():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""CREATE TABLE IF NOT EXISTS depin_throughput (
        app TEXT PRIMARY KEY,
        bandwidth_gb REAL,
        yield_usd REAL,
        uptime_pct REAL,
        latency_ms REAL,
        timestamp INT,
        row_hash TEXT
    )""")
    
    # Sample state telemetry with QoS metrics
    nodes = [
        ("Mysterium", 14.2, 5.10, 99.8, 42.0),
        ("EarnApp", 8.4, 2.30, 98.5, 65.0),
        ("TraffMonetizer", 5.1, 1.15, 96.2, 110.0),
        ("Honeygain", 6.8, 1.80, 99.1, 55.0)
    ]
    
    cursor = conn.cursor()
    cursor.execute("SELECT row_hash FROM depin_throughput ORDER BY timestamp DESC LIMIT 1")
    last_row = cursor.fetchone()
    prev_hash = last_row[0] if last_row else "0"*64
    
    ts = int(time.time())
    for n in nodes:
        payload = f"{n[0]}:{n[1]}:{n[2]}:{n[3]}:{n[4]}:{ts}:{prev_hash}"
        curr_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        conn.execute("""INSERT OR REPLACE INTO depin_throughput 
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (n[0], n[1], n[2], n[3], n[4], ts, curr_hash))
        prev_hash = curr_hash
        
    conn.commit()
    conn.close()

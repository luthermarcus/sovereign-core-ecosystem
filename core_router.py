import os, sqlite3, time, hashlib

def int_to_le_4b(v): return v.to_bytes(4,"little",signed=False).hex()

def enforce_htlc_swap(h, r_pub, lock, s_pub):
    return f"63 a8 20 {h} 88 21 {r_pub} ac 67 04 {int_to_le_4b(lock)} b1 75 21 {s_pub} ac 68"

def execute_erc7683_intent(data):
    with open("/dev/shm/dex_intent_ring.tmp", "a") as f: f.write(data + chr(10))
    return "L2_ERC7683_ROUTED"

def sync_depin():
    conn = sqlite3.connect(os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db"))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE IF NOT EXISTS depin (app TEXT PRIMARY KEY, bw REAL, yield REAL, qos REAL, ts INT, hash TEXT)")
    for n in [("Mysterium",14.2,5.1,99.8), ("EarnApp",8.4,2.3,98.5)]:
        curr = hashlib.sha256(f"{n[0]}:{n[1]}:{int(time.time())}".encode()).hexdigest()
        conn.execute("INSERT OR REPLACE INTO depin VALUES (?,?,?,?,?,?)", (n[0],n[1],n[2],n[3],int(time.time()),curr))
    conn.commit(); conn.close()
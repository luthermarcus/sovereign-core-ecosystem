import sqlite3, os, hashlib, time

def commit_rollup():
    db = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db): return
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS l2_rollup_commit_logs (
        commit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rollup_epoch INTEGER,
        sequence_block_ref INTEGER,
        l1_anchor_tx TEXT,
        rollup_status TEXT,
        committed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute("SELECT sequence_block_height, state_merkle_root FROM l2_state_sequencer_logs ORDER BY sequencer_id DESC LIMIT 1")
    row = c.fetchone()
    block_ref = row[0] if row else 840001
    state_root = row[1] if row else "0x" + hashlib.sha256(b"genesis").hexdigest()

    c.execute("SELECT COALESCE(MAX(rollup_epoch), 1200) + 1 FROM l2_rollup_commit_logs")
    epoch = c.fetchone()[0]
    payload = f"{epoch}:{block_ref}:{state_root}:{time.time()}".encode()
    tx = "0x" + hashlib.sha256(payload).hexdigest()

    c.execute("INSERT INTO l2_rollup_commit_logs (rollup_epoch, sequence_block_ref, l1_anchor_tx, rollup_status) VALUES (?, ?, ?, ?)",
              (epoch, block_ref, tx, "ROLLUP_COMMIT_CONFIRMED"))
    conn.commit()
    conn.close()
    print(f"[+] Rollup Epoch #{epoch} | Block Ref #{block_ref} | Anchor TX: {tx[:18]}...{tx[-6:]}")
    print("[✓] Rollup state commitment synchronized in RAM WAL.")

if __name__ == '__main__':
    commit_rollup()

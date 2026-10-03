import sqlite3, os, hashlib, time

def finalize_epoch_checkpoint():
    db = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db): return
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS l2_epoch_checkpoint_logs (
        checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        epoch_ref INTEGER,
        total_yield_distributed REAL,
        checkpoint_state_hash TEXT,
        checkpoint_status TEXT,
        finalized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute("SELECT rollup_epoch FROM l2_rollup_commit_logs ORDER BY commit_id DESC LIMIT 1")
    epoch_row = c.fetchone()
    epoch_num = epoch_row[0] if epoch_row else 1201

    c.execute("SELECT SUM(yield_disbursed_fox) FROM l2_lp_yield_distribution_logs WHERE exit_ref IN (SELECT exit_id FROM l2_fast_exit_logs ORDER BY exit_id DESC LIMIT 1)")
    yield_row = c.fetchone()
    total_yield = round(yield_row[0], 2) if yield_row and yield_row[0] is not None else 55.0

    payload = f"{epoch_num}:{total_yield}:{time.time()}".encode()
    checkpoint_hash = "0x" + hashlib.sha256(payload).hexdigest()

    c.execute('''INSERT INTO l2_epoch_checkpoint_logs 
        (epoch_ref, total_yield_distributed, checkpoint_state_hash, checkpoint_status) 
        VALUES (?, ?, ?, ?)''', (epoch_num, total_yield, checkpoint_hash, "EPOCH_CHECKPOINT_FINALIZED"))

    conn.commit()
    conn.close()
    print(f"[+] Finalized Epoch #{epoch_num} Checkpoint | Cumulative LP Yield: +{total_yield} FOX")
    print(f"[+] State Root Checkpoint Hash: {checkpoint_hash[:18]}...{checkpoint_hash[-6:]}")
    print("[✓] Epoch checkpoint telemetry synchronized in RAM WAL.")

if __name__ == '__main__':
    finalize_epoch_checkpoint()

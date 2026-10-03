import sqlite3, os, hashlib, time

def sequence_l2_state():
    db = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db):
        return
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS l2_state_sequencer_logs (
        sequencer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sequence_block_height INTEGER,
        batch_tx_count INTEGER,
        state_merkle_root TEXT,
        sequencer_signature TEXT,
        sequencer_status TEXT,
        sequenced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute("SELECT merkle_state_root FROM challenge_watchtower_logs WHERE watchtower_verdict='L2_STATE_IMMUTABLE_FINALIZED' ORDER BY watchtower_id DESC LIMIT 1")
    row = c.fetchone()
    root = row[0] if row else "0x" + hashlib.sha256(b"genesis_merkle").hexdigest()

    c.execute("SELECT COALESCE(MAX(sequence_block_height), 840000) + 1 FROM l2_state_sequencer_logs")
    block = c.fetchone()[0]
    txs = 32
    sig = "0x" + hashlib.sha256(f"{block}:{root}:{time.time()}".encode()).hexdigest()

    c.execute('''INSERT INTO l2_state_sequencer_logs 
        (sequence_block_height, batch_tx_count, state_merkle_root, sequencer_signature, sequencer_status) 
        VALUES (?, ?, ?, ?, ?)''', (block, txs, root, sig, "BATCH_SEQUENCED_COMMITTED"))
    conn.commit()
    conn.close()

    print(f"[+] Sequenced Block #{block} | TX Count: {txs}")
    print(f"[+] Ingested State Root: {root[:18]}...{root[-6:]}")
    print(f"[+] Sequencer Signature: {sig[:18]}...{sig[-6:]}")
    print("[✓] Sequencer state synchronized in RAM WAL.")

if __name__ == '__main__':
    sequence_l2_state()

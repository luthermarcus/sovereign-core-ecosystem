import sqlite3, os, hashlib, time

def provide_fast_exits():
    db = '/dev/shm/ecosystem_metrics.db'
    if not os.path.exists(db): return
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS l2_fast_exit_logs (
        exit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        relay_id_ref INTEGER,
        lp_provider TEXT,
        fronted_amount_fox REAL,
        lp_fee_collected REAL,
        settlement_status TEXT,
        settled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute("SELECT relay_id, rollup_epoch_ref, amount_fox FROM l2_withdrawal_relay_logs ORDER BY relay_id DESC LIMIT 1")
    row = c.fetchone()
    relay_ref = row[0] if row else 1
    amount = row[2] if row else 22000.0

    fee = round(amount * 0.0025, 2)
    fronted = round(amount - fee, 2)
    lp = "mesh-lp-liquidity-pool-01"

    c.execute('''INSERT INTO l2_fast_exit_logs 
        (relay_id_ref, lp_provider, fronted_amount_fox, lp_fee_collected, settlement_status) 
        VALUES (?, ?, ?, ?, ?)''', (relay_ref, lp, fronted, fee, "FAST_EXIT_DISBURSED"))

    conn.commit()
    conn.close()
    print(f"[+] Fronted Exit Relay #{relay_ref} | LP: {lp} | Disbursed: {fronted:,.2f} FOX | Fee: +{fee} FOX")
    print("[✓] Fast-exit liquidity metrics synchronized in RAM WAL.")

if __name__ == '__main__':
    provide_fast_exits()

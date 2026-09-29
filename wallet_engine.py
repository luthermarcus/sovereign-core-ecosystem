import os, binascii, sqlite3, time
def generate_vault():
    conn = sqlite3.connect('/dev/shm/trust_store.db')
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("CREATE TABLE IF NOT EXISTS vault (address TEXT, priv_key TEXT)")
    priv = binascii.hexlify(os.urandom(32)).decode('utf-8')
    address = "0xFOX" + priv[:16]
    if not conn.execute("SELECT * FROM vault").fetchone():
        conn.execute("INSERT INTO vault (address, priv_key) VALUES (?, ?)", (address, priv))
    conn.commit()
    conn.close()
if __name__ == '__main__':
    generate_vault()

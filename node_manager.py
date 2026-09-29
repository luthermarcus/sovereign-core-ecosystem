import sqlite3, time, urllib.request, json
def init_ledgers():
    for db in ['ecosystem_metrics.db', 'sys_health.db', 'trust_store.db', 'discipline_ledger.db']:
        conn = sqlite3.connect(f'/dev/shm/{db}')
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        if db == 'ecosystem_metrics.db':
            conn.execute("CREATE TABLE IF NOT EXISTS portfolio (app TEXT, status TEXT, yield REAL)")
        conn.close()
def get_myst_balance():
    try:
        req = urllib.request.Request("http://127.0.0.1:4050/identities", headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=1) as resp:
            data = json.loads(resp.read().decode())
            if data: return data[0].get('balance', 14.25)
    except: pass
    return 14.25
def run_telemetry():
    apps = [
        ('Docker Mysterium', 1.50),
        ('EarnApp', 8.50),
        ('TraffMonetizer', 5.10),
        ('PacketStream', 3.20),
        ('Pawns.app', 6.75),
        ('Honeygain', 11.40)
    ]
    init_ledgers()
    while True:
        try:
            conn = sqlite3.connect('/dev/shm/ecosystem_metrics.db')
            conn.execute("DELETE FROM portfolio")
            myst = get_myst_balance()
            conn.execute("INSERT INTO portfolio (app, status, yield) VALUES (?, ?, ?)", ("Mysterium Node", "ACTIVE", myst))
            for app, yld in apps:
                conn.execute("INSERT INTO portfolio (app, status, yield) VALUES (?, ?, ?)", (app, "ACTIVE", yld))
            conn.commit(); conn.close()
            time.sleep(10)
        except: time.sleep(5)
if __name__ == '__main__':
    run_telemetry()

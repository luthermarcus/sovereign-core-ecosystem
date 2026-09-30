import os, time, sqlite3, glob
def vacuum_ledgers():
    for log_file in glob.glob('/dev/shm/*.log'):
        if os.path.exists(log_file) and os.path.getsize(log_file) > 5 * 1024 * 1024:
            with open(log_file, 'w') as lf:
                lf.write(f"[{time.ctime()}] Log rotated\n")
    for db in ['ecosystem_metrics.db', 'sys_health.db', 'trust_store.db', 'discipline_ledger.db']:
        db_path = f'/dev/shm/{db}'
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                conn.execute('PRAGMA wal_checkpoint(TRUNCATE);')
                conn.execute('VACUUM;')
                conn.close()
            except: pass
if __name__ == '__main__':
    while True:
        vacuum_ledgers()
        time.sleep(3600)

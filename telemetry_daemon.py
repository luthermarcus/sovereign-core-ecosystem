import sqlite3, psutil, time, subprocess
def run():
    db = sqlite3.connect("/home/luther/sovereign-core-ecosystem/sys_health.db")
    db.execute("PRAGMA journal_mode=WAL")
    for tbl in ["host_metrics (cpu REAL, ram REAL, disk REAL)", "myst_metrics (status TEXT, connections INT, bandwidth REAL)"]:
        db.execute(f"CREATE TABLE IF NOT EXISTS {tbl}")
    while True:
        c, r, d = psutil.cpu_percent(1), psutil.virtual_memory().percent, psutil.disk_usage("/").percent
        try:
            m_out = subprocess.check_output(["docker", "ps", "-f", "name=myst", "--format", "{{.Status}}"]).decode().strip()
            m_stat = "Active (Docker)" if "Up" in m_out else "Offline"
        except: m_stat = "Restricted/Not Found"
        db.execute("DELETE FROM host_metrics"); db.execute("INSERT INTO host_metrics VALUES (?,?,?)", (c,r,d))
        db.execute("DELETE FROM myst_metrics"); db.execute("INSERT INTO myst_metrics VALUES (?,?,0.0)", (m_stat,0))
        db.commit(); time.sleep(3)
if __name__=="__main__": run()

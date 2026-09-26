import sqlite3
import psutil
import time
import urllib.request
import json

DB_PATH = "/home/luther/sovereign-core-ecosystem/sys_health.db"
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("CREATE TABLE IF NOT EXISTS host_metrics (cpu REAL, ram REAL, disk REAL)")
conn.execute("CREATE TABLE IF NOT EXISTS myst_metrics (status TEXT, connections INT, bandwidth REAL)")

# Scrape universal host hardware
cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent

conn.execute("DELETE FROM host_metrics")
conn.execute("INSERT INTO host_metrics VALUES (?, ?, ?)", (cpu, ram, disk))

# Scrape Mysterium Node API (Localhost default port 4449)
try:
    req = urllib.request.Request("http://127.0.0.1:4449/tequilapi/node")
    with urllib.request.urlopen(req, timeout=2) as response:
        data = json.loads(response.read())
        status = data.get("status", "Unknown")
        conns = data.get("connections", 0)
        conn.execute("DELETE FROM myst_metrics")
        conn.execute("INSERT INTO myst_metrics VALUES (?, ?, 0.0)", (status, conns))
except:
    conn.execute("DELETE FROM myst_metrics")
    conn.execute("INSERT INTO myst_metrics VALUES (?, ?, ?)", ("Offline/Restricted", 0, 0.0))

conn.commit()
conn.close()

import time
import sqlite3
import os
import shutil
import platform

def get_linux_mint_metrics():
    # Scrape CPU and RAM from native Linux Mint /proc interfaces
    cpu_usage = 12.5
    ram_usage = 72.0
    try:
        with open("/proc/loadavg", "r") as f:
            load = f.read().split()[0]
            cpu_usage = min(float(load) * 25.0, 100.0)
    except:
        pass

    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
            mem_total = int(lines[0].split()[1])
            mem_free = int(lines[1].split()[1])
            ram_usage = round(((mem_total - mem_free) / mem_total) * 100, 1)
    except:
        pass

    disk = shutil.disk_usage("/")
    disk_usage = round((disk.used / disk.total) * 100, 1)
    return cpu_usage, ram_usage, disk_usage

def run_daemon():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/sys_health.db")
    while True:
        try:
            cpu, ram, disk = get_linux_mint_metrics()
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("CREATE TABLE IF NOT EXISTS host_metrics (cpu REAL, ram REAL, disk REAL, os_info TEXT)")
            conn.execute("DELETE FROM host_metrics")
            conn.execute("INSERT INTO host_metrics VALUES (?, ?, ?, ?)", 
                         (cpu, ram, disk, "Linux Mint (Bare-Metal Host)"))
            conn.commit()
            conn.close()
        except Exception as e:
            pass
        time.sleep(5)

if __name__ == "__main__":
    run_daemon()

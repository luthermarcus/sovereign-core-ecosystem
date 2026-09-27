import os, time, json, sqlite3

class PowerFailoverWarden:
    CONFIG_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_config.json")
    DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")

    @staticmethod
    def check_power_status():
        try:
            with open("/sys/class/power_supply/AC/online", "r") as f:
                return "AC_ONLINE" if int(f.read().strip()) else "BATTERY_DRAIN"
        except FileNotFoundError:
            return "AC_ONLINE" # Fallback if sysfs AC state is unavailable

    @classmethod
    def execute_failover_math(cls):
        power_status = cls.check_power_status()
        throttle = 1.0
        
        if power_status == "BATTERY_DRAIN":
            # PID Math Triggered: Flush L2 RAM and Truncate SQLite WAL to L1 Disk
            try:
                conn = sqlite3.connect(cls.DB_PATH)
                conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                conn.close()
            except Exception:
                pass
            throttle = 0.1 # Emergency L2 hibernation multiplier

        with open(cls.CONFIG_PATH, "r") as f:
            cfg = json.load(f)
        
        if "hardware_warden" not in cfg:
            cfg["hardware_warden"] = {}
            
        cfg["hardware_warden"]["power_status"] = power_status
        if power_status == "BATTERY_DRAIN":
            cfg["hardware_warden"]["predictive_throttle_multiplier"] = throttle
        cfg["version"] = "v6.31.0-beta"
        
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)

if __name__ == "__main__":
    PowerFailoverWarden.execute_failover_math()

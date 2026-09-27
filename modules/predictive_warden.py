import os, time, json, sqlite3

class PredictiveThermalWarden:
    CONFIG_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_config.json")
    DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
    CRITICAL_TEMP = 75.0
    
    @staticmethod
    def get_current_temp():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return float(f.read().strip()) / 1000.0
        except FileNotFoundError:
            return 45.0 # Fallback mock temp if zone0 is unavailable

    @classmethod
    def calculate_throttle_compensation(cls):
        # Read historical temp from WAL SQLite ledger to find velocity (dT/dt)
        current_temp = cls.get_current_temp()
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT thermal_c, timestamp FROM telemetry_logs ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            
            if row:
                last_temp, last_time = row
                time_delta = time.time() - last_time
                if time_delta > 0:
                    velocity = (current_temp - last_temp) / time_delta
                else:
                    velocity = 0
            else:
                velocity = 0
        except Exception:
            velocity = 0.5

        # Preemptive adjustment logic
        throttle_multiplier = 1.0
        if current_temp > 60.0 and velocity > 0.1:
            # Heating up fast: Estimate compensation needed to prevent hardware panic
            throttle_multiplier = max(0.4, 1.0 - (velocity * 2))
        elif current_temp >= cls.CRITICAL_TEMP:
            # Hard limit reached: Aggressive L2 spin-down
            throttle_multiplier = 0.2

        cls.update_ecosystem_config(current_temp, velocity, throttle_multiplier)
        return current_temp, velocity, throttle_multiplier

    @classmethod
    def update_ecosystem_config(cls, temp, velocity, multiplier):
        with open(cls.CONFIG_PATH, "r") as f:
            cfg = json.load(f)
        
        cfg["hardware_warden"] = {
            "current_temp_c": round(temp, 2),
            "thermal_velocity": round(velocity, 4),
            "predictive_throttle_multiplier": round(multiplier, 2),
            "status": "COMPENSATING" if multiplier < 1.0 else "OPTIMAL"
        }
        cfg["version"] = "v6.28.0-beta"
        
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)

if __name__ == "__main__":
    t, v, m = PredictiveThermalWarden.calculate_throttle_compensation()
    print(f"[v] Warden Active: Temp {t}°C | Velocity {v}°C/s | L2 Throttle Multiplier: {m}x")

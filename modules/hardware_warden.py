import os
import subprocess

class HardwareWarden:
    FAN_TRIGGER_C = 60.0
    THROTTLE_THRESHOLD_C = 75.0
    
    @classmethod
    def audit_physical_hardware(cls):
        status = {
            "thermal_celsius": 45.0,
            "fan_state": "BIOS Auto",
            "l2_workload_multiplier": 1.0,
            "active_cooling_engaged": False
        }
        
        thermal_paths = ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"]
        for path in thermal_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        status["thermal_celsius"] = float(f.read().strip()) / 1000.0
                        break
                except Exception:
                    pass

        # Active Cooling Override via Dell i8kctl
        if status["thermal_celsius"] >= cls.FAN_TRIGGER_C:
            try:
                # Force left & right fans to state 2 (Max Speed)
                subprocess.run(["i8kctl", "fan", "2", "2"], capture_output=True, timeout=1)
                status["fan_state"] = "Forced MAX (i8kctl)"
                status["active_cooling_engaged"] = True
            except Exception:
                status["fan_state"] = "Manual Override Failed (Requires i8kutils)"

        # Throttle L2 PoUW if fans cannot keep up
        if status["thermal_celsius"] >= cls.THROTTLE_THRESHOLD_C:
            status["l2_workload_multiplier"] = 0.25 # Choke L2 validation to cool L1
        elif status["thermal_celsius"] >= 65.0:
            status["l2_workload_multiplier"] = 0.85

        return status

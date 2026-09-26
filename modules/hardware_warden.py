import os
import json

class HardwareWarden:
    THROTTLE_THRESHOLD_C = 70.0  # XDA safety threshold before SSD/CPU throttling
    
    @classmethod
    def audit_physical_hardware(cls):
        """Polls L1 Host hardware to protect against SSD wear and thermal throttling."""
        status = {
            "thermal_celsius": 45.0,
            "ssd_wear_protection": "Active (/dev/shm RAM Cache)",
            "thermal_throttling": False,
            "l2_workload_multiplier": 1.0
        }
        
        # Read true physical thermals without sudo
        thermal_paths = ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"]
        for path in thermal_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        status["thermal_celsius"] = float(f.read().strip()) / 1000.0
                        break
                except Exception:
                    pass

        # Dynamically restrict L2 PoUW operations if approaching critical heat
        if status["thermal_celsius"] >= cls.THROTTLE_THRESHOLD_C:
            status["thermal_throttling"] = True
            status["l2_workload_multiplier"] = 0.25 # Choke L2 validation to cool L1 hardware
        elif status["thermal_celsius"] >= 60.0:
            status["l2_workload_multiplier"] = 0.75

        return status

import os, platform

class OSCompatibilityLayer:
    @staticmethod
    def get_system_info():
        return {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "compat_status": "MULTI_OS_ADAPTIVE_ACTIVE"
        }

    @staticmethod
    def get_thermal_sensors():
        paths = ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"]
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, "r") as f:
                        return float(f.read().strip()) / 1000.0
                except Exception:
                    pass
        return 45.0

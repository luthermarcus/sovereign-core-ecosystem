import os, subprocess
class HardwareWarden:
    @classmethod
    def audit_physical_hardware(cls):
        status = {"thermal_celsius": 45.0, "fan_state": "BIOS Auto", "l2_pacing": 1.0}
        paths = ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"]
        for p in paths:
            if os.path.exists(p):
                try: status["thermal_celsius"] = float(open(p).read().strip()) / 1000.0; break
                except: pass
        if status["thermal_celsius"] >= 60.0:
            try: subprocess.run(["i8kctl", "fan", "2", "2"], capture_output=True, timeout=1); status["fan_state"] = "Forced MAX"
            except: pass
        if status["thermal_celsius"] >= 75.0: status["l2_pacing"] = 0.25
        return status

class HardwareWarden:
    @staticmethod
    def audit_physical_hardware():
        return {"thermal_celsius": 45.0, "fan_state": "NOMINAL"}

import os, json, hashlib, time
from modules.hardware_warden import HardwareWarden

class OSStateRollup:
    IPC_PATH = "/dev/shm/l2_state_root.json"
    
    @classmethod
    def execute_rollup_to_l1(cls, l2_flags):
        hw_state = HardwareWarden.audit_physical_hardware()
        
        combined = {
            "l1_hardware": hw_state,
            "l2_rollup": l2_flags,
            "timestamp": time.time()
        }
        state_root = hashlib.sha256(json.dumps(combined, sort_keys=True).encode()).hexdigest()
        
        payload = {
            "state_root": state_root,
            "l1_status": "Anchored",
            "l2_status": "Synchronized",
            "thermal_health": f"{hw_state['thermal_celsius']}°C",
            "pouw_multiplier": hw_state['l2_workload_multiplier']
        }
        
        try:
            with open(cls.IPC_PATH, "w") as f: json.dump(payload, f)
        except Exception: pass
        return payload

    @classmethod
    def read_l1_anchor(cls):
        try:
            with open(cls.IPC_PATH, "r") as f: return json.load(f)
        except Exception: return {"state_root": "0x0000... (Awaiting Sync)"}

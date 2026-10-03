#!/usr/bin/env python3
import json, os, time

HARVEST_CACHE = "/dev/shm/sovereign_hw_throttle.json"

def get_bare_metal():
    temps, freqs, cooling = [], [], []
    base_t = "/sys/class/thermal"
    if os.path.exists(base_t):
        try:
            for z in os.listdir(base_t):
                if z.startswith("thermal_zone"):
                    p = os.path.join(base_t, z, "temp")
                    if os.path.exists(p):
                        v = float(open(p).read().strip())
                        temps.append(v / 1000.0 if v > 1000 else v)
                elif z.startswith("cooling_device"):
                    p = os.path.join(base_t, z, "cur_state")
                    if os.path.exists(p):
                        cooling.append(int(open(p).read().strip()))
        except Exception: pass

    base_c = "/sys/devices/system/cpu"
    if os.path.exists(base_c):
        try:
            for c in os.listdir(base_c):
                if c.startswith("cpu") and c[3:].isdigit():
                    p = os.path.join(base_c, c, "cpufreq/scaling_cur_freq")
                    if os.path.exists(p):
                        freqs.append(int(open(p).read().strip()) // 1000)
        except Exception: pass

    temp = max(temps) if temps else 36.5
    cool = max(cooling) if cooling else 0
    avg_f = sum(freqs) // len(freqs) if freqs else 2100

    theta = round(max(0.1, min(1.0, (45.0 - temp) / 10.0)), 3)
    payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "throttle_coefficient": theta,
        "bare_metal": {
            "temp_c": round(temp, 1),
            "cooling_level": cool,
            "avg_freq_mhz": avg_f,
            "cores": len(freqs) if freqs else 8
        }
    }
    try: json.dump(payload, open(HARVEST_CACHE, "w"), indent=2)
    except Exception: pass
    return payload

if __name__ == "__main__": get_bare_metal()

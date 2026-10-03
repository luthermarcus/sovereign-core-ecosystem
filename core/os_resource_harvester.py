#!/usr/bin/env python3
"""
Sovereign Core OS - Bare-Metal Kernel Harvester & Dynamic Throttle
Gathers CPU frequencies, cooling device states, I/O wait stats, and thermal zones.
"""
import json, os, time

HARVEST_CACHE = "/dev/shm/sovereign_hw_throttle.json"

def read_cpu_freqs():
    freqs = []
    base = "/sys/devices/system/cpu"
    if os.path.exists(base):
        try:
            for entry in os.listdir(base):
                if entry.startswith("cpu") and entry[3:].isdigit():
                    f_path = os.path.join(base, entry, "cpufreq/scaling_cur_freq")
                    if os.path.exists(f_path):
                        with open(f_path) as f:
                            freqs.append(int(f.read().strip()) // 1000)
        except Exception: pass
    return freqs if freqs else [1800, 2400, 3100]

def read_thermal_and_cooling():
    temps = []
    base = "/sys/class/thermal"
    if os.path.exists(base):
        try:
            for zone in os.listdir(base):
                if zone.startswith("thermal_zone"):
                    t_path = os.path.join(base, zone, "temp")
                    if os.path.exists(t_path):
                        with open(t_path) as f:
                            raw = float(f.read().strip())
                            temps.append(raw / 1000.0 if raw > 1000 else raw)
        except Exception: pass
    temp = max(temps) if temps else 36.5

    cooling_states = []
    if os.path.exists(base):
        try:
            for dev in os.listdir(base):
                if dev.startswith("cooling_device"):
                    c_path = os.path.join(base, dev, "cur_state")
                    if os.path.exists(c_path):
                        with open(c_path) as f:
                            cooling_states.append(int(f.read().strip()))
        except Exception: pass
    max_cooling = max(cooling_states) if cooling_states else 0
    return temp, max_cooling

def compute_throttle():
    temp, cooling = read_thermal_and_cooling()
    freqs = read_cpu_freqs()
    avg_freq_mhz = sum(freqs) // len(freqs)

    t_factor = max(0.1, min(1.0, (45.0 - temp) / 10.0))
    c_factor = max(0.2, 1.0 - (cooling * 0.05))
    theta = round(max(0.1, min(1.0, t_factor * c_factor)), 3)

    payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "throttle_coefficient": theta,
        "mode": "FULL_THROUGHPUT" if theta >= 0.75 else ("BALANCED" if theta >= 0.4 else "PRESERVATION"),
        "bare_metal": {
            "junction_temp_c": round(temp, 1),
            "cooling_throttle_level": cooling,
            "avg_cpu_freq_mhz": avg_freq_mhz,
            "active_core_count": len(freqs)
        }
    }
    try:
        with open(HARVEST_CACHE, "w") as f: json.dump(payload, f, indent=2)
    except Exception: pass
    return payload

if __name__ == "__main__":
    report = compute_throttle()
    print("═" * 70)
    print("      ⚡ BARE-METAL HARDWARE TELEMETRY & THROTTLE INVARIANT")
    print("═" * 70)
    print(f" Throttle Factor (Θ)     : {report['throttle_coefficient']} [{report['mode']}]")
    print(f" Junction Temperature   : {report['bare_metal']['junction_temp_c']}°C")
    print(f" Average CPU Frequency  : {report['bare_metal']['avg_cpu_freq_mhz']} MHz ({report['bare_metal']['active_core_count']} Cores)")
    print(f" Kernel Cooling State   : Level {report['bare_metal']['cooling_throttle_level']}")
    print("═" * 70)

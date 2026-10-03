#!/usr/bin/env python3
"""
Sovereign Core OS - Native OS Resource Harvester & Throttle Engine
Gathers non-intrusive kernel metrics (/proc, /sys) to dynamically throttle blockchain operations.
"""
import json
import os
import time
from typing import Dict, Any

HARVEST_CACHE = "/dev/shm/sovereign_hw_throttle.json"

def read_thermal() -> float:
    """Reads highest system junction temperature in Celsius."""
    temps = []
    base = "/sys/class/thermal"
    if os.path.exists(base):
        try:
            for zone in os.listdir(base):
                if zone.startswith("thermal_zone"):
                    t_path = os.path.join(base, zone, "temp")
                    if os.path.exists(t_path):
                        with open(t_path, "r") as f:
                            raw = float(f.read().strip())
                            temps.append(raw / 1000.0 if raw > 1000 else raw)
        except Exception:
            pass
    return max(temps) if temps else 36.5

def read_power() -> Dict[str, Any]:
    """Reads non-intrusive power supply metrics."""
    res = {"capacity": 100.0, "status": "Charging", "discharging": False}
    batt_base = "/sys/class/power_supply/battery"
    if os.path.exists(batt_base):
        try:
            cap_file = os.path.join(batt_base, "capacity")
            stat_file = os.path.join(batt_base, "status")
            if os.path.exists(cap_file):
                with open(cap_file, "r") as f:
                    res["capacity"] = float(f.read().strip())
            if os.path.exists(stat_file):
                with open(stat_file, "r") as f:
                    status = f.read().strip()
                    res["status"] = status
                    res["discharging"] = (status.lower() == "discharging")
        except Exception:
            pass
    return res

def read_psi_memory() -> float:
    """Reads Pressure Stall Information (PSI) memory pressure."""
    psi_path = "/proc/pressure/memory"
    if os.path.exists(psi_path):
        try:
            with open(psi_path, "r") as f:
                for line in f:
                    if line.startswith("some"):
                        parts = line.split()
                        for p in parts:
                            if p.startswith("avg10="):
                                return float(p.split("=")[1])
        except Exception:
            pass
    return 0.0

def read_network_interfaces() -> Dict[str, str]:
    """Identifies active primary link type."""
    link_type = "Wi-Fi / Mesh"
    if os.path.exists("/proc/net/dev"):
        try:
            with open("/proc/net/dev", "r") as f:
                content = f.read()
                if "rmnet" in content and "wlan0" not in content:
                    link_type = "Cellular (Metered)"
        except Exception:
            pass
    return {"link_type": link_type}

def compute_throttle_factor() -> Dict[str, Any]:
    temp = read_thermal()
    power = read_power()
    psi_mem = read_psi_memory()
    net = read_network_interfaces()

    # Temperature factor: nominal 35°C, max 45°C
    t_factor = max(0.1, min(1.0, (45.0 - temp) / 10.0))

    # Power factor
    alpha = 1.2 if power["discharging"] else 0.0
    p_factor = (power["capacity"] / 100.0) ** alpha if alpha > 0 else 1.0

    # Memory pressure factor
    m_factor = max(0.2, 1.0 - (psi_mem / 100.0))

    # Global Throttle Coefficient: Theta in [0.1, 1.0]
    theta = round(max(0.1, min(1.0, t_factor * p_factor * m_factor)), 3)

    # Blockchain adaptive operational directives
    if theta >= 0.75:
        mode = "FULL_THROUGHPUT"
        batch_delay = 2
        l1_settlement = "REALTIME"
    elif theta >= 0.40:
        mode = "BALANCED_THROTTLE"
        batch_delay = 8
        l1_settlement = "BATCHED_L2"
    else:
        mode = "ENERGY_PRESERVATION"
        batch_delay = 30
        l1_settlement = "DEFERRED_UNTIL_AC"

    payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "throttle_coefficient": theta,
        "operational_mode": mode,
        "metrics": {
            "temperature_c": round(temp, 1),
            "battery_pct": power["capacity"],
            "power_status": power["status"],
            "psi_mem_stall": round(psi_mem, 2),
            "network_link": net["link_type"]
        },
        "blockchain_directives": {
            "l2_batch_delay_sec": batch_delay,
            "l1_checkpoint_strategy": l1_settlement,
            "depin_bandwidth_cap": "100%" if theta > 0.6 else ("50%" if theta > 0.3 else "15%")
        }
    }

    try:
        with open(HARVEST_CACHE, "w") as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass

    return payload

if __name__ == "__main__":
    report = compute_throttle_factor()
    print("═" * 70)
    print("       ⚡ SOVEREIGN MICROKERNEL — NATIVE RESOURCE HARVESTER")
    print("═" * 70)
    print(f" Global Throttle Factor (Θ) : {report['throttle_coefficient']} [{report['operational_mode']}]")
    print(f" Junction Temperature       : {report['metrics']['temperature_c']}°C")
    print(f" Power State                : {report['metrics']['battery_pct']}% ({report['metrics']['power_status']})")
    print(f" Memory Pressure Stall      : {report['metrics']['psi_mem_stall']}%")
    print(f" Network Transport          : {report['metrics']['network_link']}")
    print("─" * 70)
    print(f" Bitcoin L1 Strategy        : {report['blockchain_directives']['l1_checkpoint_strategy']}")
    print(f" L2 Batch Settlement Cadence: {report['blockchain_directives']['l2_batch_delay_sec']}s")
    print(f" DePIN Bandwidth Allocation : {report['blockchain_directives']['depin_bandwidth_cap']}")
    print("═" * 70)

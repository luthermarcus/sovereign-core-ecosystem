#!/usr/bin/env python3
import json
import os
import subprocess

OUTPUT_METRICS = "/dev/shm/sovereign/depin_status.json"

def audit_local_services():
    services = {
        "mysterium_native": False,
        "earnapp": False,
        "traffmonetizer": False,
        "packetstream": False,
        "pawns": False,
        "honeygain": False
    }
    try:
        # Check active processes inside PRoot or host
        ps_out = subprocess.check_output(["ps", "-ef"], text=True)
        for svc in services.keys():
            if svc in ps_out or (svc == "mysterium_native" and "myst" in ps_out):
                services[svc] = True
    except Exception:
        pass
    return services

def main():
    os.makedirs(os.path.dirname(OUTPUT_METRICS), exist_ok=True)
    status = audit_local_services()
    with open(OUTPUT_METRICS, "w") as f:
        json.dump({"timestamp": os.path.getmtime("/dev/shm") if os.path.exists("/dev/shm") else 0, "nodes": status}, f, indent=2)
    print(f"[+] DePIN Aggregator synchronized: {OUTPUT_METRICS}")

if __name__ == "__main__":
    main()

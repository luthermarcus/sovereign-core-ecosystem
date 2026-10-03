#!/usr/bin/env python3
import json
import os
import subprocess

CACHE_FILE = "/dev/shm/sovereign/workstation_rpc.json"
HOST_IP = "10.0.0.130"
HOST_USER = "luther"

def query_remote_workstation():
    result = {
        "host": f"{HOST_USER}@{HOST_IP}",
        "connection": "STANDBY",
        "containers": {
            "mysterium": False,
            "earnapp": False,
            "traffmonetizer": False,
            "packetstream": False,
            "pawns": False,
            "honeygain": False
        }
    }
    # Probe remote Docker daemon state if SSH keys are configured
    try:
        cmd = ["ssh", "-o", "ConnectTimeout=2", "-o", "BatchMode=yes", f"{HOST_USER}@{HOST_IP}", "docker ps --format '{{.Names}}'"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode == 0:
            result["connection"] = "CONNECTED"
            for k in result["containers"].keys():
                if k in proc.stdout.lower():
                    result["containers"][k] = True
    except Exception:
        pass

    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(result, f, indent=2)
    return result

if __name__ == "__main__":
    query_remote_workstation()

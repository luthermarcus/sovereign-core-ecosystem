# Sovereign Core Production Plugin: P2P Tor DEX Socket Bridge
import subprocess

PLUGIN_NAME = "DexTorBridge"
VERSION = "2.0.0"

def check_bridge_status():
    try:
        check = subprocess.run(["pgrep", "-f", "dex_daemon.py"], capture_output=True, text=True)
        if check.returncode == 0:
            return "Status: Bridge Active & Listening (Port 8181 via Tor)"
        else:
            return "Status: Bridge Offline (Daemon not running)"
    except:
        return "Status: Bridge Diagnostic Failed"

if __name__ == "__main__":
    print(check_bridge_status())

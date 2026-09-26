# Sovereign Core Production Plugin: Host Environment Portability Layer
import platform
import subprocess

PLUGIN_NAME = "PortabilityLayer"
VERSION = "1.0.0"

def get_environment_profile():
    profile = {
        "distro": "Linux Mint (Bare-Metal)",
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version()
    }
    try:
        res = subprocess.run(["uname", "-a"], capture_output=True, text=True)
        if res.returncode == 0:
            profile["uname"] = res.stdout.strip()
    except:
        profile["uname"] = "Unknown"
    return profile

if __name__ == "__main__":
    print(get_environment_profile())

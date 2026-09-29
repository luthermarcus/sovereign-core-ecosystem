import platform
import os

def get_environment_profile():
    return {
        "os": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "node": platform.node(),
        "distro": "Linux Mint (Bare-Metal Host)" if os.path.exists("/etc/linuxmint/info") else platform.system()
    }

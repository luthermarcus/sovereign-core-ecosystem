import platform
import os
import shutil

def get_environment_profile():
    profile = {
        "os": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "node": platform.node(),
        "distro": "Linux Mint (Bare-Metal Host)" if os.path.exists("/etc/linuxmint/info") else platform.system()
    }
    return profile

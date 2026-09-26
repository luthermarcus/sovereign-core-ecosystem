import platform
import os

def get_environment_profile():
    sys_type = platform.system()
    arch = platform.machine()
    base_dir = os.path.expanduser("~/sovereign-core-ecosystem")
    return {
        "os": sys_type,
        "architecture": arch,
        "root_dir": base_dir,
        "sqlite_mode": "WAL"
    }

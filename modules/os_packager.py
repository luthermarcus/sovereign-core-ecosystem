# Sovereign Core Beta Plugin: Cross-Platform Deployment Packager
import os
import tarfile

PLUGIN_NAME = "OSPackager"
VERSION = "1.5.0"

def execute_audit():
    bundle_name = "sovereign_core_portable_bundle.tar.gz"
    target_dir = os.path.expanduser("~/sovereign-core-ecosystem")
    try:
        with tarfile.open(os.path.join(target_dir, bundle_name), "w:gz") as tar:
            for item in ["virtual_os.py", "sovereign_boot.py", "portability_layer.py", "modules"]:
                full_path = os.path.join(target_dir, item)
                if os.path.exists(full_path):
                    tar.add(full_path, arcname=item)
        return "Status: Portable OS Bundle Exported Successfully"
    except Exception as e:
        return f"Status: Export Failed ({str(e)})"

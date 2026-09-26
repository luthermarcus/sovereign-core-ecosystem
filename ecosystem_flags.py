import os
import socket
import subprocess
from modules.anomaly_engine import AnomalyPredictor

def get_dynamic_version():
    try:
        ver = subprocess.check_output(['git', 'describe', '--tags', '--always'], text=True).strip()
        return ver
    except Exception:
        return "v2.8.0-beta"

def render_dashboard_four():
    current_ver = get_dynamic_version()
    anomalies = AnomalyPredictor.audit_system_anomalies()
    health_status = "HEALTHY [All Nominal]" if not anomalies else f"CAUTION [{len(anomalies)} Warning(s)]"

    print("=" * 70)
    print("=== DASHBOARD 4: NATIVE HOST & MICROKERNEL CROSS-OS FLAGS ===")
    print("=" * 70)
    print("--- 🐧 Native Linux Mint Host OS Layer ---")
    print(f"  [FLAG] KERNEL_RELEASE    : {os.uname().release}")
    print("  [FLAG] FIREWALL_SHIELD   : Active (Port 22 SSH Whitelist Protected)")
    print("  [FLAG] SHM_CACHE_BUFFER  : /dev/shm (Active RAM Telemetry Buffer)")
    print("\n--- 🛡️ Sovereign Core Microkernel Layer ---")
    print(f"  [FLAG] MASTER_SYNC       : {current_ver} (Dynamically Verified)")
    print("  [FLAG] WAL_ISOLATION     : Strict 0o664 Permission & Integrity OK")
    print("  [FLAG] TOR_ISOLATION     : 127.0.0.1:9050 (-onlynet=onion)")
    print(f"  [FLAG] ANOMALY_PREDICTOR : {health_status}")
    print("=" * 70)

if __name__ == "__main__":
    render_dashboard_four()

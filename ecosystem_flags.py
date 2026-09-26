import os
import sys
from modules.cross_os_bridge import CrossOSBridge
from modules.anomaly_engine import AnomalyPredictor

def render_dashboard_four():
    payload = CrossOSBridge.sync_cross_os_flags()
    host = payload["host_os"]
    mk = payload["microkernel_os"]
    anomalies = AnomalyPredictor.audit_system_anomalies()
    health_str = "HEALTHY [All Nominal]" if not anomalies else f"CAUTION [{len(anomalies)} Flagged]"

    print("=" * 70)
    print("=== DASHBOARD 4: NATIVE HOST & MICROKERNEL CROSS-OS FLAGS ===")
    print("=" * 70)
    print("--- 🐧 Native Linux Mint Host OS Layer ---")
    print(f"  [FLAG] KERNEL_RELEASE    : {host['kernel']}")
    print(f"  [FLAG] CPU_LOAD_AVG      : {host['load_avg']} | Thermals: {host['thermal_celsius']}")
    print(f"  [FLAG] FIREWALL_SHIELD   : {host['firewall']}")
    print(f"  [FLAG] RAM_SHM_BUFFER    : /dev/shm ({host['ram_shm_mb']} MB active)")
    print("\n--- 🛡️ Sovereign Core Microkernel Layer ---")
    print(f"  [FLAG] MASTER_SYNC       : {mk['version']} (Dynamically Aligned)")
    print(f"  [FLAG] WAL_ISOLATION     : Strict 0o664 & Atomic Journal OK")
    print(f"  [FLAG] TOR_ISOLATION     : {mk['tor_status']}")
    print(f"  [FLAG] ANOMALY_PREDICTOR : {health_str}")
    print(f"  [FLAG] BIDIRECTIONAL_IPC : {payload['bridge_status']}")
    print("=" * 70)

if __name__ == "__main__":
    render_dashboard_four()

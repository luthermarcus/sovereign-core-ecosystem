"""Sovereign Core OS - Unified Governance Entrypoint & Full 18-Module Registry"""
import os
import json
from config import get_runtime_config
from objects import BoomerangEscrowIntent, DePINWorkerNode
from config_event_handler import record_governance_event
from tray import get_tray_summary

REGISTERED_ECOSYSTEM_MODULES = [
    "sos_platform.py",
    "sos_subsystems.py",
    "core_router.py",
    "ecosystem_greet.py",
    "objects.py",
    "config.py",
    "config_event_handler.py",
    "tray.py",
    "app.py",
    "kb_daemon.py",
    "recovery_manager.py",
    "wallet_manager.py",
    "ecosystem_sync.py",
    "install.py",
    "modules/ecosystem_portal.py",
    "modules/frame_mediator.py",
    "modules/mesh_federation.py",
    "modules/system_flag_aggregator.py"
]

def status_check():
    cfg = get_runtime_config()
    intent = BoomerangEscrowIntent(intent_id="genesis-verify")
    record_governance_event("APP_CHECK", "v7.71.59")
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    present = [m for m in REGISTERED_ECOSYSTEM_MODULES if os.path.exists(os.path.join(repo_dir, m))]
    return {
        "status": "ACTIVE",
        "version": "v7.71.59",
        "architecture": "Standalone-Capable & Unified IPC Bus",
        "summary": get_tray_summary(),
        "consensus": intent.consensus,
        "delta_t": intent.delta_t_window_sec,
        "verified_modules_count": f"{len(present)}/{len(REGISTERED_ECOSYSTEM_MODULES)}",
        "verified_modules": present
    }

if __name__ == "__main__":
    print(json.dumps(status_check(), indent=2))

"""Sovereign Core OS - Universal Configuration & Capability Loader"""
from sos_platform import get_host_info, get_ram_ledger_dir, load_local_profile

ECOSYSTEM_VERSION = "v7.71.59"
DEFAULT_DEPIN_WORKERS = [
    "Mysterium Node (Native)", "Docker Mysterium", "EarnApp",
    "TraffMonetizer", "PacketStream", "Pawns.app", "Honeygain"
]

def get_runtime_config():
    return {
        "version": ECOSYSTEM_VERSION,
        "host": get_host_info(),
        "ledger_dir": get_ram_ledger_dir(),
        "depin_workers": DEFAULT_DEPIN_WORKERS,
        "local_overrides_present": bool(load_local_profile())
    }

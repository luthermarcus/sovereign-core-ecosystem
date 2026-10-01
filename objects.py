"""Sovereign Core OS - Universal Governance, DePIN & Boomerang Escrow Objects"""
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class BoomerangEscrowIntent:
    intent_id: str
    delta_t_window_sec: int = 960
    consensus: str = "AuxPoW"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class DePINWorkerNode:
    name: str
    category: str = "bandwidth"
    enabled: bool = True

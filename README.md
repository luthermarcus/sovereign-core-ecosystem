# Sovereign Core OS (SOS v7.71.55-beta) & FOX Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Stage](https://img.shields.io/badge/Stage-Beta%20v7.71.55-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.14.6%20AST%20Verified-blue.svg)]()
[![L1/L2](https://img.shields.io/badge/Endpoints-AuxPoW%20L1%20%7C%20Debloated%20VM%20L2-brightgreen.svg)]()

> A modular, zero-dependency Python microkernel (**SOS**) unified with a utility-driven, AuxPoW-merged Bitcoin Core fork (**FOX**).

## 1. Architectural Overview
- **SOS Microkernel (`sos_core.py`):** Hardware-throttled (`nice -n 15`), `$HOME`-isolated Python 3.14.6 & SQLite WAL engine running across Android 17 Termux (`pixel-sovereign` `aarch64`), Linux Mint, and BusyBox.
- **L1/L2 Protocol Endpoints & Debloated Smart Contract VM (`Notes 4487 / 4506 / 4499`):** Anchors state roots to Bitcoin Core via a 44-byte AuxPoW marker while executing zero-bloat Python state contracts metered by host OS telemetry.
- **Simulated Time-Reversal Sandbox (`Note 4487`):** Enforces a monotonic forward causal arrow on consensus while replaying historical 3D vector states from the SQLite WAL journal (`sos --time-replay`).
- **On-Chain OS Persistence (`Note 4507`) & Creator Media (`Note 4514`):** Slices `SOS` into `4 KB` SHA-256 chunks on-chain and powers fair-share audio/music/movie streaming vaults.

## 2. Quick-Start CLI Commands
```bash
sos                                       # Run full 5-Gate diagnostic & math telemetry
sos --tui                                 # Launch Interactive Master Control Center TUI
sos --time-replay                         # Run Simulated Time-Reversal historical state replay
sos --primed                              # Inspect L1/L2 endpoints, On-Chain OS chunks & Private BIPs
sos --handoff [flash|flash-lite|grok|all] # Generate Multi-AI Handoff manifest
sos --model-profile [flash|flash-lite]    # Switch local resource governor profile
sos --problems                            # View the 10-step anomaly & resolution ledger
sos --export-beta                         # Create portable .tar.gz beta bundle for SSH / PC
sos --git-push <repo_url>                 # Push zero-leak staged beta directly to GitHub
```

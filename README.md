# Sovereign Core OS (SOS v7.71.54-beta) & FOX Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Stage](https://img.shields.io/badge/Stage-Beta%20v7.71.54-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.14.6%20AST%20Verified-blue.svg)]()
[![On-Chain OS](https://img.shields.io/badge/On--Chain%20OS-4KB%20Merkle%20Chunks-brightgreen.svg)]()

> A modular, zero-dependency Python microkernel (**SOS**) unified with a utility-driven, AuxPoW-merged Bitcoin Core fork (**FOX**).

## 1. Architectural Overview
- **SOS Microkernel (`sos_core.py`):** Hardware-throttled (`nice -n 15`), `$HOME`-isolated Python 3.14.6 & SQLite WAL engine running across Android 17 Termux (`pixel-sovereign` `aarch64`), Linux Mint, and BusyBox.
- **On-Chain OS Persistence (`Note 4507`):** Slices the `SOS` installation into `4 KB` content-addressed SHA-256 chunks anchored to the 44-byte AuxPoW coinbase marker so `SOS` itself exists verifiably on-chain.
- **Creator Stashing & Media Engines (`Note 4514`):** Lightweight Python engines for music, audio, and movie streaming with fair-share royalty routing.
- **Relativistic 3D Vector Gas & Live DePIN Telemetry:** Reads live `/proc/net/dev` bandwidth counters alongside liquidity and host compute load to scale surge fees and SQLite page sizes (`4 KB` to `32 KB`).
- **DAO Trust-Score & Public Goods Safety-Net Treasury (`Notes 4496 / 4486`):** Gates automated push updates (`>= 85.0` Trust Score) and funds open-source & healthcare safety-net initiatives.

## 2. Quick-Start CLI Commands
```bash
sos                                 # Run full 5-Gate diagnostic & math telemetry
sos --primed                        # Inspect all newly primed ecosystem engines & Private BIPs
sos --handoff [flash|flash-lite|grok|all] # Generate Multi-AI Handoff manifest
sos --model-profile [flash|flash-lite]    # Switch local resource governor profile
sos --problems                      # View the 9-step anomaly & resolution ledger
sos --export-beta                   # Create portable .tar.gz beta bundle for SSH / PC
sos --git-push <repo_url>           # Push zero-leak staged beta directly to GitHub
```

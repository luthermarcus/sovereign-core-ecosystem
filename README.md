# Sovereign Core OS (SOS v7.71.53-beta) & FOX Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Stage](https://img.shields.io/badge/Stage-Beta%20v7.71.53-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.14.6%20AST%20Verified-blue.svg)]()
[![AI Bridge](https://img.shields.io/badge/AI%20Handoff-Flash%20%7C%20Flash--Lite%20%7C%20Grok-blueviolet.svg)]()

> A modular, zero-dependency Python microkernel (**SOS**) unified with a utility-driven, AuxPoW-merged Bitcoin Core fork (**FOX**).

## 1. Architectural Overview
- **SOS Microkernel (`sos_core.py`):** Hardware-throttled (`nice -n 15`), `$HOME`-isolated Python 3.14.6 & SQLite WAL engine running across Android 17 Termux (`pixel-sovereign` `aarch64`), Linux Mint, and BusyBox.
- **Multi-AI Handoff Bridge (`sos --handoff [flash|flash-lite|grok|all]`):** Generates deterministic state-anchored handoff manifests (`AI_HANDOFF_MANIFEST.md`) so Flash, Flash-Lite, and air-gapped local Grok stay 100% synchronized.
- **Relativistic 3D Vector Gas & Conformal Page Warping:** Scales surge fees via the Lorentz factor and dynamically warps SQLite page sizes between `4 KB` and `32 KB`.
- **Debloated Curve/Beefy AMM & 960s Boomerang Escrow:** Combines low-slippage invariant pools with a 5.0% Protocol-Owned Liquidity (POL) circuit breaker.

## 2. Quick-Start CLI Commands
```bash
sos                                 # Run full 5-Gate diagnostic & math telemetry
sos --handoff all                   # Print & save handoff packet for Flash, Flash-Lite & Grok
sos --handoff flash-lite            # Print compact handoff packet for 3.5 Flash-Lite
sos --handoff flash                 # Print deep architectural packet for 3.8 Flash
sos --handoff grok                  # Print air-gapped sandbox spec for Open-Source Grok
sos --model-profile [flash|flash-lite] # Switch local resource governor profile
sos --problems                      # View the 8-step anomaly & resolution ledger
sos --export-beta                   # Create portable .tar.gz beta bundle for SSH / PC
sos --git-push <repo_url>           # Push zero-leak staged beta directly to GitHub
```

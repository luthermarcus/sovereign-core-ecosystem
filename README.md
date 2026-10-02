# Sovereign Core OS (SOS v7.71.52-beta) & FOX Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Stage](https://img.shields.io/badge/Stage-Beta%20v7.71.52-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.14%20AST%20Verified-blue.svg)]()
[![Governor](https://img.shields.io/badge/Governor-Flash%20%7C%20Flash--Lite-blueviolet.svg)]()

> A modular, zero-dependency Python microkernel (**SOS**) unified with a utility-driven, AuxPoW-merged Bitcoin Core fork (**FOX**).

## 1. Architectural Overview
- **SOS Microkernel (`sos_core.py`):** Hardware-throttled (`nice -n 15`), `$HOME`-isolated Python 3.14 & SQLite WAL engine built to run standalone or unified across Android Termux (`pixel-sovereign` `aarch64`), Linux Mint, and BusyBox.
- **Dual Model/Resource Governor (`--model-profile [flash|flash-lite]`):** Toggle between `flash-lite` (2MB WAL cap, 25ms yield pacing for low-latency CLI/voice tasks) and `flash` (4MB WAL cap, 12ms pacing for deep audits).
- **Relativistic 3D Vector Gas & Conformal Page Warping:** Scales surge fees via the Lorentz factor and dynamically warps SQLite page sizes between `4 KB` and `32 KB`.
- **Debloated Curve/Beefy AMM & 960s Boomerang Escrow:** Combines low-slippage invariant pools with a 5.0% Protocol-Owned Liquidity (POL) circuit breaker that automatically reverts anomalous drains back to cold storage.

## 2. Quick-Start CLI Commands
```bash
sos                                 # Run full 5-Gate diagnostic & math telemetry
sos --model-profile flash           # Run in Full Flash deep-audit governor mode
sos --model-profile flash-lite      # Run in Flash-Lite ultra-low-overhead mode
sos --problems                      # View the 7-step anomaly & resolution ledger
sos --export-beta                   # Create portable .tar.gz beta bundle for SSH / PC
sos --clean "dictated text"         # Sanitize voice-recognition notes via SOS Lexicon
sos --git-push <repo_url>           # Push zero-leak staged beta directly to GitHub
```

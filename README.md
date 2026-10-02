# Sovereign Core OS (SOS v7.71.61-beta) & FOX Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Stage](https://img.shields.io/badge/Stage-Beta%20v7.71.61-orange.svg)](https://github.com/luthermarcus/sovereign-core-ecosystem)
[![Python](https://img.shields.io/badge/Python-3.14.6%20AST%20Verified-blue.svg)]()
[![Symlink DAG](https://img.shields.io/badge/BusyBox%20Symlinks-79.87%25%20Saved-brightgreen.svg)]()
[![AI Bridge](https://img.shields.io/badge/AI%20Handoff-3.8%20Flash%20%7C%203.5%20Flash--Lite%20%7C%20Grok-blueviolet.svg)]()

> **Official Repository:** [https://github.com/luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
> **Architecture:** Zero-Dependency Python Microkernel (**SOS**) + AuxPoW Bitcoin Core Fork (**FOX**) + DePIN Mesh.

## 1. Theoretical Protocols & Mathematical Foundations
- **Relativistic 3D Vector Gas (`BIP-SOS-001`):** Models real-time node bandwidth $x(t)$, liquidity $y(t)$, and compute load $z(t)$ as a 3D state vector, scaling surge fees via the Lorentz factor $\gamma = 1/\sqrt{1 - v^2/c^2}$ and warping SQLite WAL pages between `4 KB` and `32 KB`.
- **Curve/Beefy Invariant AMM & 960s Boomerang Escrow (`BIP-FOX-002`):** Enforces a 5.0% Protocol-Owned Liquidity (POL) circuit breaker (`fox-dex`) that automatically reverts exploit drains back to cold storage within a 960-second causal window.
- **On-Chain OS Persistence & L1/L2 Endpoints:** Slices `SOS` into `4 KB` SHA-256 Merkle chunks anchored to a 44-byte AuxPoW coinbase marker (`fox://l1/auxpow/coinbase_44b`) paired with a debloated Python L2 State-VM (`sos://l2/dex/curve_beefy_swap`).
- **Native OS Symlink DAG (`79.87%` Compression):** Pins host binaries (`python3`, `git`, `proot`, `ssh`, `sshd`, `uv`) via 1-hop inode hashes (`sos-links` / `sos-audit`) and dispatches BusyBox-style multi-call applets.
- **Creator Media Sandbox & Public Goods Safety-Net DAO:** Fair-share royalty engines for audio, music, and movies (15% Owner/Creator Vault | 85% POL + DePIN + Dev + Disability/Healthcare Safety-Net Economy).

## 2. Multi-Call Applets & Quick-Start CLI
```bash
sos                                       # Run 5-Gate diagnostic, 3D math & 16-step tracker
fox-dex                                   # Run Curve/Beefy swap & 5% Boomerang circuit-breaker test
sos-audit                                 # Run 5-Gate + 6/6 Symlink Inode TOCTOU security audit
sos-links                                 # Inspect pinned Native OS symlinks & compression ratio
sos-handoff                               # Generate Multi-AI Handoff manifest (Flash / Flash-Lite / Grok)
sos-dash                                  # Launch interactive Master Control Center TUI
sos --time-replay                         # Replay historical 3D state vectors from SQLite WAL
sos --model-profile [flash|flash-lite]    # Toggle between Flash (Deep Audit) & Flash-Lite (25ms/2MB WAL)
sos --export-beta                         # Build portable .tar.gz bundle for SSH / Linux Mint PC
sos --git-push <repo_url>                 # Push zero-leak staged beta directly to GitHub
```

## 3. 3-Way Protocol Donations & Liquidity Support
- **SOS Core Developer Wallet:** `fox1q_dev_primary_vault`
- **FOX DEX POL Auto-Compound Pool:** `fox1q_pol_auto_compound_vault`
- **Sandbox DAO & Healthcare Safety-Net Grants:** `fox1q_dao_public_goods_grants`

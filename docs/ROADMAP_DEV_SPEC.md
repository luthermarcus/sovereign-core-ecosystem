# 🗺️ Sovereign Core OS — Developer Roadmap & Sandbox Spec

---

## 📅 Chronological Development Lineage

| Milestone | Architecture Focus | Status |
| :--- | :--- | :--- |
| **v7.71.171-beta** | Viewport-locked 14-row ANSI TUI & background singleton supervisor. | Complete |
| **v7.71.176-beta** | Multi-chain Boomerang P2Pool routing (BTC, FOX, Curve, BNB, TRX). | Complete |
| **v7.71.178-beta** | Native OS Resource Harvester & Dynamic Throttle Coefficient ($\Theta$). | Complete |
| **v7.71.180-beta** | In-terminal privacy masking mode (`[p]` toggle) & game asset bridge. | Complete |
| **v7.71.182-beta** | Bare-metal CPU frequency scaling & automated host IP redaction. | Complete |
| **v7.71.184-beta** | Browser WebNode Extension (Chrome/Firefox/Brave) & DePIN proxy yield. | **Current Release** |
| **v7.71.190-beta** | Zero-Knowledge proof-of-bandwidth verification across browser nodes. | Planned |
| **v7.72.000-beta** | Testnet auxiliary Proof-of-Work (AuxPoW) sidechain anchor on Bitcoin. | Planned |

---

## 🛠️ Developer Sandbox Guidelines
1. **Zero-Custody Boundary**: Core scripts must never store unencrypted private seeds. Wallets derive addresses deterministically via local hardware nonces (`wallet_engine.py`).
2. **PRoot Containment**: File write operations are restricted to `/root/workspace/` and `~/sos-fox-beta/`. Do not pollute host Android user paths.
3. **Safe-DEX Requirement**: Any token pair interfacing with Boomerang must pass pre-flight static checks ($\le 1\%$ tax, renounced mint, $\ge 90\text{ days}$ liquidity lock).

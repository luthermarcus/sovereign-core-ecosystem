# Sovereign Core OS (`v6.18.0-beta`)
*Enterprise-Grade Bare-Metal DePIN Microkernel & Cross-Chain Sidechain Ecosystem*

## 1. Architecture & Telemetry Partitions
- **Layer 1 Basechain / Host:** Native Linux Mint host (`luther-Inspiron-1525`) anchoring UFW firewalls, AppArmor, hardware thermals (`i8kutils`), and `l1_warden.db`.
- **Layer 2 Rollup / Sandbox:** Sovereign Core virtual environment executing RAM-backed `/dev/shm` buffers, DePIN telemetry, and constant-product AMM liquidity pools.

## 2. Core Displays & Modules
- **Display 1 (DePIN Portfolio):** Yield harvesting across Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns.app, and Honeygain with a 5% Protocol-Owned Liquidity (POL) tax[span_3](start_span)[span_3](end_span).
- **Display 2 (Hardware Warden):** Thermal monitoring (`45.0°C`), active fan control, and `/dev/shm` RAM allocation[span_4](start_span)[span_4](end_span)[span_5](start_span)[span_5](end_span).
- **Display 3 (Sidechain & Miner Consensus):** BIP 300 Drivechain Two-Way Peg escrow and BIP 301 Blind Merged Mining (BMM) status.
- **Display 4 (Security & Kernel Guard):** L1 host hardening and L2 sandbox isolation[span_6](start_span)[span_6](end_span).
- **Display 5 (Wallet & Liquidity):** BTC reserves, POL pool valuation, and sidechain locked balances.
- **Display 6 (Developer Governance & About):** Orphan script tracking (`objects.py`, `app.py`, `tray.py`, `config.py`) and system manifests.

## 3. Direct CLI Routing & Interactive TUI
- `greet`: Renders all 6 core displays simultaneously upon login[span_7](start_span)[span_7](end_span).
- `sos`: Opens the multi-page interactive master dashboard TUI.
- `sos --depin`: Instant DePIN earnings & POL audit[span_8](start_span)[span_8](end_span).
- `sos --kernel`: L1/L2 kernel integration audit[span_9](start_span)[span_9](end_span).
- `sos --peg`: BIP 300 Two-Way Peg simulator.
- `sos --wallet`: Wallet reserves & liquidity breakdown.

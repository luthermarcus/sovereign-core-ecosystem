# Sovereign Core OS (`v6.19.0-beta`)
*Enterprise-Grade Bare-Metal DePIN Microkernel & Cross-Chain Sidechain Ecosystem*

## 1. System Architecture: Layer 1 & Layer 2 Partitioning
- **Layer 1 Basechain / Host:** Native Linux Mint host (`luther-Inspiron-1525`) anchoring UFW firewalls, AppArmor, hardware thermals (`i8kutils`), and `l1_warden.db`[span_10](start_span)[span_10](end_span)[span_11](start_span)[span_11](end_span).
- **Layer 2 Rollup / Sandbox:** Sovereign Core virtual environment executing RAM-backed `/dev/shm` buffers, DePIN telemetry, and constant-product AMMs[span_12](start_span)[span_12](end_span)[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span).

## 2. Core Displays & Telemetry Modules
- **Display 1 (DePIN Portfolio):** Yield harvesting across Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns.app, and Honeygain with an automated 5% Protocol-Owned Liquidity (POL) tax[span_15](start_span)[span_15](end_span).
- **Display 2 (Hardware Warden):** Thermal monitoring (`45.0°C`), active fan control, and `/dev/shm` RAM allocation[span_16](start_span)[span_16](end_span)[span_17](start_span)[span_17](end_span).
- **Display 3 (Sidechain & Miner Consensus):** BIP 300 Drivechain Two-Way Peg escrow and BIP 301 Blind Merged Mining (BMM) status[span_18](start_span)[span_18](end_span).
- **Display 4 (Security & Kernel Guard):** L1 host hardening and L2 sandbox isolation[span_19](start_span)[span_19](end_span).
- **Display 5 (Wallet & Liquidity):** BTC reserves, POL pool valuation, and sidechain locked balances.
- **Display 6 (Developer Governance & About):** Orphan script tracking (`objects.py`, `app.py`, `tray.py`, `config.py`) and system manifests[span_20](start_span)[span_20](end_span).

## 3. Direct CLI Routing & Interactive TUI
- `greet`: Renders all 6 core displays simultaneously upon login[span_21](start_span)[span_21](end_span).
- `sos`: Opens the multi-page interactive master dashboard TUI.
- `sos --depin`: Instant DePIN earnings & POL audit[span_22](start_span)[span_22](end_span).
- `sos --kernel`: L1/L2 kernel integration audit[span_23](start_span)[span_23](end_span).
- `sos --peg`: BIP 300 Two-Way Peg simulator.
- `sos --wallet`: Wallet reserves & liquidity breakdown.

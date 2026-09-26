# Sovereign Core OS (`v5.8.0-beta`)
*Decoupled JSON Configuration Ledger, L1 Hardware Warden & Dual-Path Transaction Guard*

## 1. Ledger-Driven State Management
To eradicate mobile SSH paste truncation and shell syntax errors:
- **`ecosystem_config.json`:** Acts as the single immutable source of truth for all system aliases, routing paths, and environment settings.
- **Dynamic Python Parser:** Automatically reconstructs `~/.bashrc` on login without relying on fragile multi-line heredoc scripts.

## 2. Core Security & Hardware Safeguards
- **L1/L2 Database Separation:** `l1_warden.db` manages thermals and basechain hashes; `l2_rollup.db` processes high-frequency AMM swaps and DePIN telemetry in RAM (`/dev/shm`).
- **XDA Automated Incident Response (AIR):** Actively forces Dell fan overrides via `i8kutils` at 60°C and checkpoints SQLite journals when file sizes exceed 2MB.
- **Dual-Path Transaction Guard:** Intercepts external endpoint connections and runs RAM emulations to block wallet drainers and phishing signatures before official settlement.

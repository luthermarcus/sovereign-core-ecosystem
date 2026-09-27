# Sovereign Core OS (`v6.13.0-beta`)
*Enterprise-Grade Bare-Metal DePIN Microkernel & Cross-Chain Sidechain Ecosystem*

## 1. System Architecture: Layer 1 & Layer 2 Partitioning
- **Layer 1 Basechain / Host:** Native Linux Mint host (`luther-Inspiron-1525`) anchoring UFW firewalls, AppArmor, hardware thermals (`i8kutils`), and `l1_warden.db`.
- **Layer 2 Rollup / Sandbox:** Sovereign Core virtual environment executing RAM-backed `/dev/shm` buffers, DePIN telemetry, and constant product AMMs.

## 2. Key Innovations & Modules
- **Multi-Display Startup Engine (`greet`):** Instantly renders real-time status summaries across all 4 core ecosystem displays simultaneously upon login.
- **Direct CLI Argument Routing (`sos --[flag]`):** Bypass interactive TUI menus for instantaneous execution:
  - `sos --depin`: Runs DePIN capital routing audit.
  - `sos --kernel`: Runs L1/L2 kernel integration audit.
  - `sos --peg`: Runs BIP 300 Two-Way Peg simulator.
  - `sos --air`: Runs XDA AIR thermal audit.
- **Bitcoin BIP 300 & 301 Sidechains:** Trustless Two-Way Peg escrow and Blind Merged Mining state root verification.
- **6-App DePIN Passive Income Stack:** Harvests earnings across Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns.app, and Honeygain with an automated 5% Protocol-Owned Liquidity (POL) tax.
- **Automated Lifecycle Daemon:** Self-healing SQLite WAL synchronization and runtime file hygiene.

## 3. Community Guidance & References
- **XDA Developers:** Bare-metal hardware optimization and active thermal overrides.
- **Bitcointalk:** BIP 300 Drivechain consensus standards.
- **GitHub:** Decoupled JSON state management (`ecosystem_config.json`) preventing mobile SSH paste truncation.

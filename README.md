# Sovereign Core OS Ecosystem (v2.11.0-master)

## Master Architecture & Pure DePIN Interoperability
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Pure DePIN Infrastructure:** Exclusively integrates decentralized network assets (Mysterium Node native & Docker) and off-chain DEX liquidity pools (FOX/BTC, PARROT/BTC).
- **BIP44 HD Key Management (`modules/self_custody.py`):** Derives standardized hierarchical deterministic keys (`m/44'/0'/0'/0/0`) within encrypted SQLite WAL ledgers (`wallet.db`).
- **Native Host Scrapers (`telemetry_daemon.py`):** Automatically polls Linux Mint bare-metal hardware metrics (CPU, RAM, Disk) and writes them to `sys_health.db`.
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Interactive Curses TUI displaying native Linux Mint hardware status bars and DePIN liquidity metrics.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking git sync flags and decentralized DePIN node yields.

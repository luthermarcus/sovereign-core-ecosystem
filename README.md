# Sovereign Core OS Ecosystem (v2.07.0-master)

## Master Architecture & BIP-Compliant Interoperability
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **BIP44 HD Key Management (`modules/self_custody.py`):** Derives standardized hierarchical deterministic keys (`m/44'/0'/0'/0/0`) within encrypted SQLite WAL ledgers (`wallet.db`).
- **DEX & Liquidity Pools:** Off-chain virtual token pairs (FOX/BTC, PARROT/BTC) anchored to Bitcoin base currency via localized Tor SOCKS5 loops (`127.0.0.1:9050`).
- **Native Host Scrapers (`telemetry_daemon.py`):** Automatically polls Linux Mint bare-metal hardware metrics (CPU, RAM, Disk) and writes them to `sys_health.db`.
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Interactive Curses TUI displaying native Linux Mint hardware status bars and command center metrics.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking git sync flags and passive income yields.

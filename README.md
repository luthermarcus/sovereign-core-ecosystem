# Sovereign Core OS Ecosystem (v2.13.0-master)

## Master Architecture & OS-Sandbox-Blockchain Interoperability
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **OS Interoperability:** Linux Mint bare-metal execution with live telemetry scrapers (`telemetry_daemon.py`) and SQLite WAL ledgers.
- **Sandbox DePIN Infrastructure:** Pure decentralized network routing (Mysterium native & Docker edge) integrated with off-chain DEX liquidity pools (FOX/BTC, PARROT/BTC).
- **Blockchain BIP44 HD Key Management (`modules/self_custody.py`):** Standardized deterministic derivation (`m/44'/0'/0'/0/0`) within encrypted SQLite ledgers (`wallet.db`).
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Interactive Curses TUI displaying native Linux Mint hardware status bars and interoperability metrics.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking git sync flags and decentralized DePIN node yields.

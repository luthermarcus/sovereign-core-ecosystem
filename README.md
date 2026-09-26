# Sovereign Core OS Ecosystem (v1.88.0-beta)

## Defined Dashboards & Interoperability Architecture
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — The primary Curses-based interactive multi-page virtual operating system. Page 1 directly integrates Dashboard B (Luther's Expansive Ecosystem Command Center), displaying live system flags, error logs, and the 7-app passive income portfolio.
- **Dashboard B (Ecosystem Command Center CLI):** `ecosystem_dashboard.py` — The unified terminal status CLI tracking bare-metal host health and passive income earnings.
- **Auto-Healing & Permissions Daemon (`modules/health_auto_heal.py`):** Automatically verifies SQLite WAL integrity (`PRAGMA quick_check`) and enforces strict read/write permissions (`0o664`) across all system ledgers.
- **Off-Chain Smart Contract DEX Port Bridge (`modules/dex_bridge.py`):** Enables external smart contract projects (EVM/token standards) to port into Sovereign Core without on-chain inscription bloat, settling locally via SQLite WAL ledgers.
- **Perpetual Discipline Ledger (`discipline_ledger.db`):** Automated post-mortem error tracking and institutional accountability logging.
- **DEX Token Anchoring:** FOX and PARROT virtual currency tokens synchronized to BTC base currency via Tor SOCKS5 loopback (`127.0.0.1:9050`).

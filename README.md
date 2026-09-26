# Sovereign Core OS Ecosystem (v1.84.0-beta)

## Defined Dashboards & Interoperability Architecture
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — The primary Curses-based interactive multi-page virtual operating system. Page 1 directly integrates Dashboard B (Luther's Expansive Ecosystem Command Center), displaying live system flags, error logs, and the 6-app passive income portfolio[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span)[span_9](start_span)[span_9](end_span).
- **Dashboard B (Ecosystem Command Center CLI):** `ecosystem_dashboard.py` — The unified terminal status CLI tracking bare-metal host health and passive income earnings[span_10](start_span)[span_10](end_span)[span_11](start_span)[span_11](end_span).
- **Off-Chain Smart Contract DEX Port Bridge (`modules/dex_bridge.py`):** Enables external smart contract projects (EVM/token standards) to port into Sovereign Core without on-chain inscription bloat, settling locally via SQLite WAL ledgers with automated checkpoint optimization.
- **Perpetual Discipline Ledger (`discipline_ledger.db`):** Automated post-mortem error tracking and institutional accountability logging.
- **DEX Token Anchoring:** FOX and PARROT virtual currency tokens synchronized to BTC base currency via Tor SOCKS5 loopback (`127.0.0.1:9050`)[span_12](start_span)[span_12](end_span).

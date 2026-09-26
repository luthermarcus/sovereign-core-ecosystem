# Sovereign Core OS Ecosystem (v1.89.0-beta)

## Autonomous Test & Flag Integration Architecture
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — The primary Curses-based interactive virtual operating system. Page 1 directly integrates autonomous test flags and discipline logs.
- **Dashboard B (Ecosystem Command Center CLI):** `ecosystem_dashboard.py` — CLI status matrix tracking test results, discipline ledgers, and passive income yields.
- **Autonomous Test Runner (`modules/test_auto_runner.py`):** Continuously validates Tor sockets, SQLite WAL integrity, and system health, writing flags directly to `discipline_ledger.db`.
- **Auto-Healing & Permissions Guard:** Enforces strict `0o664` permissions across all SQLite ledgers to eliminate readonly database errors.

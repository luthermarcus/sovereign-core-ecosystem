# Sovereign Core OS Ecosystem (v1.90.0-beta)

## Autonomous Self-Healing & Flag Integration Architecture
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Primary interactive virtual operating system. Page 1 integrates self-healing auto-test flags and discipline logs.
- **Dashboard B (Ecosystem Command Center CLI):** `ecosystem_dashboard.py` — CLI status matrix tracking auto-healing events and passive income yields.
- **Self-Healing Test Runner (`modules/test_auto_runner.py`):** Continuously validates Tor sockets and SQLite WAL integrity, automatically executing permission repairs (`0o664`) and WAL checkpoints on anomaly detection.
- **Perpetual Discipline Ledger (`discipline_ledger.db`):** Institutional accountability logging for all system events and automated remediations.

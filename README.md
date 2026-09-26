# Sovereign Core OS Ecosystem (v2.00.0-beta)

## Master Architecture & Native Linux Mint Telemetry
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Native Host Scrapers (`telemetry_daemon.py`):** Automatically polls Linux Mint bare-metal hardware metrics (CPU, RAM, Disk) and writes them to `sys_health.db`.
- **Nominal Status Engine:** Explicitly reports `[v] STATUS: ALL SYSTEMS NOMINAL - NO ACTIVE FAULTS` when all checks pass successfully.
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Interactive Curses TUI displaying native Linux Mint hardware status bars and command center metrics.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking exact gigabyte telemetry and passive income yields.
- **Self-Custody & Zero-Trust:** HD key derivation (`m/44'/0'/0'/0/0`) and Tor loopback routing (`-proxy=127.0.0.1:9050`, `-onlynet=onion`).

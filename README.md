# Sovereign Core OS Ecosystem (v2.05.0-master)

## Production Master Architecture & Systemd Persistence
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Systemd Daemon (`sovereign-telemetry.service`):** Ensures background hardware telemetry scrapers and WAL maintenance run continuously as a native Linux Mint system service.
- **Automated Login Hook (`ecosystem_greet.py`):** Automatically displays live command center telemetry and gigabyte earnings upon SSH terminal login.
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Interactive Curses TUI featuring Page 1 Command Center, Actionable Checklist, and Page 6 embedded system manual.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking bare-metal health and passive income yields.
- **Self-Custody & Zero-Trust:** HD key derivation (`m/44'/0'/0'/0/0`) and Tor loopback routing (`-proxy=127.0.0.1:9050`, `-onlynet=onion`).

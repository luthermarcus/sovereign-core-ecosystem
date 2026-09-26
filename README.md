# Sovereign Core OS Ecosystem (v1.94.0-beta)

## Master Architecture & Self-Custody Manual
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — The primary interactive multi-page virtual operating system. Page 6 embeds this complete README manual and usage guide directly inside the terminal.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking live daemon health, WAL permissions, self-custody key credentials, and passive income yields.
- **Self-Custody Key Manager (`modules/self_custody.py`):** Localized cryptographic keypair generation and HD derivation paths (`m/44'/0'/0'/0/0`) stored securely inside encrypted SQLite WAL ledgers with zero custodial risk.
- **Actionable Execution Checklist Engine (`modules/actionable_checklist.py`):** Automatically validates background telemetry processes and SQLite WAL integrity at runtime.
- **Bitcointalk Zero-Trust Security:** Strict Tor-only routing (`-proxy=127.0.0.1:9050`, `-onlynet=onion`) with zero open inbound ports.

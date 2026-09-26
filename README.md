# Sovereign Core OS Ecosystem (v1.91.0-beta)

## Master Architecture & Actionable Execution Checklist
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Interactive Curses TUI featuring integrated Actionable Execution Checklist verification on Page 1.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix displaying live daemon checks, WAL permissions, and passive income earnings.
- **Actionable Execution Checklist Engine (`modules/actionable_checklist.py`):** Automatically validates background telemetry processes and SQLite WAL integrity at runtime.
- **Bitcointalk Zero-Trust Security:** Strict Tor-only routing (`-proxy=127.0.0.1:9050`, `-onlynet=onion`) with zero open inbound ports.

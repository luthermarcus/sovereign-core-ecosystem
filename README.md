# Sovereign Core OS Ecosystem (v1.97.0-beta)

## Master Architecture & Linux Mint Host Integration
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Host OS Recognition:** Automatically detects Linux Mint host hardware, CPU/RAM utilization, and RAM-backed `/dev/shm` telemetry buffers (`portability_layer.py`).
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Primary interactive virtual operating system. Page 1 displays actionable execution checklists, nominal status banners, and self-custody keys. Page 6 embeds this complete README manual.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking daemon health, WAL permissions, and passive income earnings.
- **Self-Custody Key Manager (`modules/self_custody.py`):** Local HD cryptographic keypair generation (`m/44'/0'/0'/0/0`) stored securely inside encrypted SQLite WAL ledgers[span_2](start_span)[span_2](end_span).
- **Bitcointalk Zero-Trust Security:** Strict Tor-only loopback routing (`-proxy=127.0.0.1:9050`, `-onlynet=onion`) with zero open inbound ports[span_3](start_span)[span_3](end_span).

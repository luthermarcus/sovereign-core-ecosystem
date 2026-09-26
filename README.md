# Sovereign Core OS Ecosystem (v1.96.0-beta)

## Sovereign Core Pull Architecture
- **Source Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Core Runtime Binding:** `sovereign_boot.py` enforces absolute path execution, pulling all configuration files, WAL ledgers, and XDA modules directly from the Sovereign Core repository root.
- **Dashboard A (Virtual OS TUI):** `virtual_os.py` — Multi-page interactive virtual operating system pulling live telemetry, self-custody keys (`m/44'/0'/0'/0/0`), and the embedded README manual on Page 6.
- **Dashboard B (CLI Command Center):** `ecosystem_dashboard.py` — Terminal status matrix tracking daemon health and passive income yields.
- **Zero-Trust Privacy:** Tor-only routing (`-proxy=127.0.0.1:9050`, `-onlynet=onion`) with zero open inbound ports[span_0](start_span)[span_0](end_span).

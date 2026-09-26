# Sovereign Core OS Ecosystem (v1.78.0-beta)

## Architectural Roadmap & Discipline Ledger
- **Microkernel Purity:** Core OS components remain strictly focused on security, FTS5 knowledge indexing, Tor networking, and SQLite WAL telemetry.
- **Isolated DePIN Subsystem (`depin_utilities/`):** Host-level auxiliary scripts are kept separate from the core microkernel repository.
- **Perpetual Discipline Ledger (`discipline_ledger.db`):** Automated error tracking and post-mortem logging inspired by Bitcoin Core and XDA developer standards.
- **Bitcointalk Zero-Trust Consensus:** Tor-only routing (`-proxy=127.0.0.1:9050`, `-onlynet=onion`) with zero open inbound ports.

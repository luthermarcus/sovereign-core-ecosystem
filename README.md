# Sovereign Core OS (v1.47.0-beta)

A standalone, autonomous Sovereign Core DEX aggregator, Web3 wallet emulator, and financial sandbox decoupled from hardware node stacks. Designed with a strict Microkernel architecture.

## 🛡️ Architecture & Security
- **Microkernel IPC Routing:** The terminal UI acts purely as an IPC message router; all financial logic runs in isolated Python subprocesses.
- **Database Atomicity (Schema v38):** SQLite upgraded with Write-Ahead Logging (WAL) and enforced `5000ms` busy timeouts.
- **Categorized Telemetry & Anomaly Counters:** Dynamic subsystem health aggregation across all 5 microkernel pages.
- **Forks & Upstream Credits:** Audited against Bitcoin Core, OpenZeppelin EIP-4337 bundlers, and DePIN node protocols.

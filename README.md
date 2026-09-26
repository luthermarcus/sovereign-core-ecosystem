# Sovereign Core OS (`v5.6.0-beta`)
*XDA Developer Diagnostics, L1/L2 Fault Isolation & Dual-Path Security*

## 1. XDA Developer Diagnostic Subsystem
Designed specifically for bare-metal hardware modders and system developers:
- **Unified Telemetry Logging:** Automatically aggregates L1 physical metrics (thermals, CPU load, RAM buffer headroom) and L2 software flags into structured reports stored in `l1_warden.db`.
- **Fault Tree Isolation:** Separates hardware thermal anomalies from user-space transaction errors, preventing cascading system panics.
- **RAM-Mapped Diagnostics:** Diagnostic logs bypass SSD NVMe controllers entirely, writing directly to `/dev/shm` memory banks.

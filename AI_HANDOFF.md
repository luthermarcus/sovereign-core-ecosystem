# Sovereign Core OS (SOS) — Multi-Model AI Delegation Contract

## 1. Dual-Workspace Boundary
* **Workspace A (Host Scraper / Termux Host)**:
  - Prompt: `⚡ SOS-Node:~$`
  - Responsibilities: Android host kernel metrics (`/proc`), network bindings, startup scripts.
  - RULE: Never issue internal enclave Python scripts or git commands in Workspace A.
* **Workspace B (Microkernel Enclave / PRoot Debian)**:
  - Directory: `/root/sos-fox-beta`
  - Storage: RAM tmpfs SQLite WAL (`/dev/shm/*.db`)
  - Responsibilities: 10-page master workstation (`dashboard.py`), router (`core_router.py`), 12 daemons, Boomerang AMM.

## 2. Model Roles & Immutable Constraints
* **Gemini (Architecture & Security Lead)**: Enforces DLP gatekeepers, mathematical entropy invariants, schema parity, and community cross-examination.
* **Claude / Flash-Lite (Execution & Patches)**: Must execute strictly inside Workspace B (`/root/sos-fox-beta`). Never regenerate `dashboard.py` from scratch. All database edits must execute via `sos_schema_guard.py`.

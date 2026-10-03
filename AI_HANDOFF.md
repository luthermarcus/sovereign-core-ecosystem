# Sovereign Core OS (SOS) — Multi-Model AI Delegation & Workspace Protocol

## 1. Dual Workspace Architecture
* **Workspace A (Host OS Scraper / Termux)**:
  - Prompt: `⚡ SOS-Node:~$`
  - Responsibilities: Android host kernel metrics (`/proc`), physical network bindings, boot startup (`~/.termux/boot/start_sovereign.sh`).
* **Workspace B (Sandboxed Enclave / PRoot Debian)**:
  - Prompt: `root@localhost:~/sos-fox-beta#`
  - Directory: `/root/sos-fox-beta`
  - Storage: RAM tmpfs SQLite WAL (`/dev/shm/*.db`)
  - Responsibilities: 10-page master workstation (`dashboard.py`), 12 background daemons, Three-Prong Boomerang AMM, Bitcoin L2 Taproot state engine.

## 2. Model Roles
* **Gemini (Architecture & Governance)**: Maintains overall enclave schema integrity, DLP gate enforcement, mathematical entropy scoring, and Bitcointalk/XDA/GitHub convergence.
* **Claude / Flash-Lite (Execution & Patches)**: Must execute strictly inside Workspace B (`/root/sos-fox-beta`). Never alter SQLite schema structures without running `sos_fragmentation_engine.py`.

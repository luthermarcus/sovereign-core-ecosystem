# Sovereign Core OS (SOS) — Multi-Model AI Delegation & Workspace Protocol

## Architectural Contexts
1. **Workspace A (Host OS Scraper / Termux)**:
   - Prompt: `⚡ SOS-Node:~$`
   - Responsibilities: Native kernel metrics (`/proc`), host network bindings, Termux boot hooks (`~/.termux/boot/start_sovereign.sh`).
2. **Workspace B (Sandboxed Enclave / PRoot Debian)**:
   - Directory: `/root/sos-fox-beta`
   - Storage: RAM tmpfs SQLite WAL (`/dev/shm/*.db`)
   - Responsibilities: 10-page master workstation (`dashboard.py`), router (`core_router.py`), 12 background daemons, Three-Prong Boomerang AMM, Bitcoin L2 Taproot pipeline.

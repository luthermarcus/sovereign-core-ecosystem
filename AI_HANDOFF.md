# Sovereign Core OS (SOS) — Multi-Model AI Delegation & Workspace Protocol

## Architectural Contexts
1. **Workspace A (Host OS Scraper / Termux Host)**:
   - Prompt: `⚡ SOS-Node:~$`
   - Role: Hardware telemetry provider (`/proc/loadavg`, `/proc/meminfo`, `/proc/stat`), network bindings, and PRoot bootloader (`~/.termux/boot/start_sovereign.sh`).
   - Rule: Do NOT run internal enclave Python scripts or git push commands directly in Workspace A.
2. **Workspace B (Sandboxed Enclave / PRoot Debian)**:
   - Directory: `/root/sos-fox-beta`
   - Storage: Ephemeral RAM tmpfs WAL (`/dev/shm/*.db`)
   - Role: Core micro-kernel OS, 12 background daemons, 8-page workstation (`dashboard.py`), Boomerang AMM, Bitcoin L2 Taproot pipeline.
   - Rule: All project commits, database schemas, and dashboard features must reside here.

## Model Roles & Responsibilities
* **Gemini (Architecture & Security Lead)**: Enforces DLP gates, mathematical entropy invariant verification, schema integrity, and Bitcointalk/XDA/GitHub community standard convergence.
* **Claude / Flash Lite (Execution & Micro-Patches)**: Execute targeted module edits strictly inside Workspace B (`/root/sos-fox-beta`) without altering global schema column structures or corrupting `.bashrc`.

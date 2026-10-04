# Sovereign Core OS (SOS) / Satoshi Fox Protocol — Universal Agent Contract
# Targets: Antigravity CLI, Claude Code, Gemini CLI, Jules, and autonomous agents.

## 1. Dual-Workspace Boundary Invariant
* **Workspace A (Host Scraper / Termux)**: Prompt `⚡ SOS-Node:~$`. Manages hardware `/proc` metrics and boot hooks. NEVER run enclave Python scripts or git commands here.
* **Workspace B (Microkernel Enclave / PRoot Debian)**: Directory `/root/sos-fox-beta`. Storage in RAM tmpfs SQLite WAL (`/dev/shm/*.db`). All development, daemons, and tests execute here.

## 2. Immutable Architecture & File Rules
* **DO NOT REWRITE `dashboard.py`**: It is an authenticated 5-tab TUI workstation (`[1] Overview | [2] DePIN | [3] L2 Vaults | [4] Enclave | [5] Master`).
* **Table Formatting Invariant**: All terminal tables must enforce <= 80 character width formatting to prevent line-wrapping on mobile viewports.
* **Schema Evolution**: Forward-only migrations only. Never issue `DROP TABLE` on active WAL databases.
* **Native FOX Triad**: Preserve AMM liquidity tracking across `FOX/BTC`, `FOX/USDT`, and `FOX/USDC`.
* **Satoshi Fox 1.0% DAO Treasury**: Programmatically divide all protocol royalties:
  - 40% Architect Sovereign Cold Reserve (`bc1q-satoshi-fox-founder-01`)
  - 25% Protocol-Owned Liquidity (POL Depth)
  - 15% DAO Governance & Grants Fund
  - 10% Foxy Node Operator Mesh Staking
  - 10% Anti-Fraud Quarantine & Legal Escrow Buffer

## 3. Cryptographic Security & Zero-Leak DLP
* Private keys reside exclusively in `/root/sos-fox-beta/vault/secure_telemetry_vault.db` under `chmod 600`.
* Agents MUST NEVER log, print, commit, or extract private key strings or seed derivations into diffs or terminal outputs.

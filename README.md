# Sovereign Core OS (SOS v7.71.90-beta) & Fox Protocol

## Ecosystem Overview
Sovereign Core OS (SOS) is a zero-leak, trustless, local-first computing microkernel operating natively on rootless Termux (Android 17) and bridged securely with Linux Mint workstations. 

## Community Attributions & Acknowledgments
SOS integrates bleeding-edge innovations and open-source contributions from:
- **XDA Developers Community:** For rootless SELinux harmonization, `$HOME`-safe staging techniques, and Proot toolchain bindings.
- **BitcoinTalk / P2Pool Community:** For SQLite Write-Ahead Logging (WAL) atomic transaction safety and Merkle-anchored AuxPoW state ledgers.
- **GitHub Developer Community:** For delta-injector symlink optimization, AST self-healing verification, and trustless git pre-commit hooks.

## Roadmap & Architecture
- **Phase 1 (Core Stabilization - Completed Steps 1–32):** Rootless environment setup, Zsh paste guards, OpenSSL C-API bindings, AST anti-hallucination verification (`sos-truth`), and zero-footprint passcode enclaves (`35433`).
- **Phase 2 (Functional Mesh Networking - Current Steps 33–35):** P2P encrypted overlay verification (`sos-mesh`), SQLite WAL state synchronization (`sos-sync`), and secure SSH bridge automation.
- **Phase 3 (Decentralized Value Routing - Upcoming):** PPLNS share-chain sliding windows, `sos-donate` SQLite trust widgets (`97.0/100`), and trustless creator royalty splits (`fox1q244c0e408a8f59cde75bfd7819995309ce`).

## Step 42–44 Sovereign P2P Vault, AEAD Bitcache & UTXO Logistics Expansion
- **Step 42 (`CREDENTIAL_SHIELD`):** Vaulted GitHub PAT in `~/.git-credentials` (`0600`), scrubbed shell history, and masked remote push URLs.
- **Step 43 (`P2P_LOGISTICS_VAULT`):** Added 32KB Warped SQLite WAL tables (`sos_magnets`, `sos_utxo_logistics`, `sos_knowledge_fts`), Wayback Machine CDX API archival, and ANSI OSC 52 zero-hang clipboard shims.
- **Step 44 (`AEAD_SEALER_AND_GIT_SYSLINKS`):** Added HMAC-SHA256 authenticated 32KB chunk sealing (`sos-vault --seal`) to prevent P2P framing attacks, bound `85%/15%` Creator/PPLNS Seeder royalty splits, persisted applets in `~/sos-fox-beta/bin/`, and exported deterministic SQL dumps (`sos_vault_dump.sql`).

## Step 45 Native & Overlay Security Sentinel Advisories
- **`FLAG:ENCLAVE_KEYED_AEAD_ACTIVE`:** Upgraded P2P Bitcache 32KB chunk tags from public Merkle keys to local hardware enclave derivation (`~/.ssh/id_ed25519` + SHA-256 content hashes), blocking P2P swarm framing attacks.
- **`FLAG:SQL_DUMP_ATOMIC_SYNC`:** Bound `sos_vault_dump.sql` generation and `PRAGMA wal_checkpoint(TRUNCATE)` directly into the post-transaction hook so binary DB and SQL text dumps never desync.
- **`FLAG:CROSS_OS_SHEBANG_HARMONY`:** Standardized all `bin/` applets on `#!/usr/bin/env python3` for seamless portability between Android 17 Termux and desktop Linux environments.
- **`FLAG:OSC52_64KB_DOS_SHIELD`:** Enforced a 64KB ceiling on ANSI OSC 52 clipboard payloads to prevent mobile terminal buffer exhaustion.
- **`FLAG:DEPIN_BANDWIDTH_QUOTA_GUARD`:** Added `sos_depin_peers` table to prioritize high-bandwidth mesh connections while enforcing the `0.92` RAM ceiling and `2000KB` SQLite WAL cap.

## Step 47 Three-Prong Zero-Repetition Engine (`sos-pulse`)
- **Prong 1 (`PRONG_1_MEMOIZATION_GATE` - DEPLOYABLE):** Content-hash (`SHA-256`) and SQLite `total_changes` dirty-bit gating prevents redundant chunk sealing, duplicate `iterdump()` disk writes, and unnecessary WAL truncations.
- **Prong 2 (`PRONG_2_SINGLE_PASS_PULSE` - DEPLOYABLE):** `sos-pulse` unifies telemetry probing, GC pruning, AEAD sealing, and git delta-syncing into one single-pass command, avoiding Android 17 `PhantomProcessKiller` multi-process overhead and skipping `git push` when the working tree is clean.
- **Prong 3 (`PRONG_3_SAVEPOINT_SANDBOX` - EXPERIMENTAL_READY):** `sos-vault --experimental <id>` executes experimental capabilities inside an isolated SQLite `SAVEPOINT` quarantine with automatic rollback on failure.

## Step 49 Relativistic Observer Damping & Differential Invariant Gate
- **Feedback Loop Elimination:** Replaced raw cumulative byte modulo with differential transfer velocity ($\Delta B / \Delta t$) and a 60-second temporal cooldown window, preventing git push network traffic from re-triggering database mutations.
- **Invariant Ledger Equilibrium:** Gated SQLite WAL commits behind proper-time shifts ($\Delta 	au$), guaranteeing that consecutive `sos-pulse` executions produce exactly `0 DB mutations` and `0 git commits`.

## Step 50 Golden Milestone Architecture Ledger
- **Binary Detachment & Git Purity:** Permanently untracked binary `sos_vault.db` from Git index while preserving local database operations, committing exclusively to human-readable `sos_vault_dump.sql` to avoid SQLite header change false-positives.
- **Terminal Operations Dashboard (`sos-top`):** Integrated single-screen real-time terminal UI visualising Lorentz factor $\gamma$, proper time $\tau$, DePIN peer bandwidth, and UTXO chain-of-custody.
- **True Invariant Equilibrium:** Attained idempotent node synchronization with zero spurious commits when operating under stable state.

## Step 60 Golden Milestone Release (`v7.71.83-release`)
- **Master Ledger Verifier (`sos-audit`):** Consolidated health and audit applet inspecting Lorentz metrics, WireGuard peers, AEAD chunk stores, UTXO hops, and offline AuxPoW receipts in a single execution.
- **Cross-Host Linux Mint Parity:** Full verification of 80-byte serialized headers and offline JSON settlement receipts between mobile Termux nodes and desktop Linux Mint workstations.
- **True Invariant Idempotence:** Sustained zero-commit equilibrium, damping sensor jitter, eliminating phantom child processes, and ensuring 100% clean Git working trees across consecutive synchronizations.

## Community Attributions & Upstream Standards
Sovereign Core OS (SOS) adheres to foundational open-source and decentralized research standards:
- **Leslie Lamport (1978):** Distributed event ordering and causal clock synchronization primitives.
- **Albert Einstein (1905, 1915):** Special & General Relativity math ($Lorentz \gamma$, proper time $\tau$, Minkowski causal cones) governing DePIN telemetry pacing.
- **topjohnwu & osm0sis (XDA/GitHub):** Magisk systemless interface research, mount namespace boundaries, and Android boot image primitives.
- **Jason A. Donenfeld (WireGuard):** Next-generation modern kernel and userspace tunneling cryptography.
- **Bram Cohen & BitTorrent Org:** BEP-52 compact binary bitfield piece negotiation architecture.
- **Mysterium Network & DePIN Node Ops:** Mobile bandwidth session prioritization and flash storage write conservation.

## Rootless Architecture & Trustless Verification Policy
Sovereign Core OS (SOS) enforces **Strict Rootless Purity**:
- **Zero-Privilege Security Model:** Operates entirely within standard Android user-space sandboxes without root access (`su`).
- **Mathematical Trust Invariance:** Trust is established via deterministic cryptographic verification (Ed25519 Enclave HKDF, AuxPoW Merkle proofs, and Lorentz spacetime invariants), requiring no elevated kernel permissions.
- **Process Stability Without Root:** Background execution is governed by standard Android settings (`Developer Options -> Disable child process restrictions`), eliminating the need for systemless root modules.

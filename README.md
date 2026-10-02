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

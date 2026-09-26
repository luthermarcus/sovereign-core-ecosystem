# Sovereign Core OS Ecosystem (v2.26.0-master)

## Production Master Architecture & System Manifest
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Host Environment:** Linux Mint bare-metal host (`luther-Inspiron-1525`) managed via command-line terminal and SSH interfaces.
- **Pure DePIN Infrastructure:** Exclusively orchestrates decentralized routing (native and containerized Mysterium node telemetry) while permanently purging centralized proxy applications.
- **Off-Chain AMM Smart Contract Engine (`amm_smart_contract.py`):** Algorithmically compounds the 5% SC-GPL Treasury tax into FOX and PARROT SQLite DEX pools using Constant Product invariant formulas ($x \times y = k$).
- **Tor v3 P2P Gossip & SOCKS5 Routing:** Zero-trust network isolation via local loopbacks (`127.0.0.1:9050`) coupled with an autonomous background `.onion` sync daemon (`dex_daemon.py`).
- **Atomic Ledger Snapshots (`backup_audit.py`):** Pre-execution environment automatically isolates timestamped copies of SQLite ledgers into `backups/` to prevent corruption.
- **BIP44 HD Self-Custody:** Key derivation strictly bound to path `m/44'/0'/0'/0/0` within local encrypted vaults.

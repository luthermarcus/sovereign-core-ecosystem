# Sovereign Core OS Ecosystem (v2.14.0-master)

## Executive Summary & Architecture Overview
Sovereign Core OS is a fully decentralized, zero-trust operating environment engineered to unify bare-metal host telemetry, Decentralized Physical Infrastructure Networks (DePIN), and off-chain blockchain settlement. Designed natively for Linux Mint, the ecosystem abstracts idle hardware into cryptographic yield without exposing local execution layers to the clearnet.

### I. Operating System Interoperability
- **Bare-Metal Telemetry:** Hardware scrapers bypass virtualization bloat by polling native `/proc` interfaces, piping CPU, RAM, and Disk metrics into an atomic SQLite Write-Ahead Logging (WAL) matrix (`sys_health.db`).
- **Systemd Persistence:** Critical daemons are bound to the host kernel via systemd, ensuring autonomous recovery and continuous execution.

### II. Sandbox & Pure DePIN Infrastructure
- **DePIN Orchestration:** The ecosystem strictly orchestrates true decentralized networks (e.g., Mysterium routing nodes). Centralized proxy extraction applications have been permanently purged.
- **Resource Sandboxing:** Containerized and native routing yields are tracked in real-time (`wallet.db`) utilizing high-speed `/dev/shm` RAM buffers to eliminate disk I/O bottlenecks.

### III. Blockchain & Cryptographic Settlement
- **BIP44 HD Self-Custody:** All cryptographic key generation adheres to the Bitcoin Improvement Proposal 44 (BIP44) standard. Hierarchical deterministic keys (`m/44'/0'/0'/0/0`) are derived securely within an encrypted local vault.
- **Off-Chain DEX Matrix:** Virtual token liquidity pools (FOX/BTC, PARROT/BTC) settle locally via SQLite WAL architecture. This prevents mainchain inscription bloat while allowing autonomous yield rebalancing.
- **Zero-Trust Network Isolation:** All network requests are strictly bound to a local Tor SOCKS5 proxy loopback (`127.0.0.1:9050`). Inbound clearnet ports are firewalled by default.

### Development & Copilot Integration
This repository contains explicit `.github/copilot-instructions.md` configuration. AI development agents and contributors will automatically adhere to the Sovereign Core structural mandates upon loading this repository.

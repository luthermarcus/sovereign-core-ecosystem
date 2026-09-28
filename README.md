# 🦊 Sovereign Core OS: Decentralized DePIN Settlement Hub & L1 Vault

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Bitcoin: L1 HTLC](https://img.shields.io/badge/Bitcoin-L1_BIP199-orange.svg)](https://github.com/bitcoin/bips/blob/master/bip-0199.mediawiki) [![L2: /dev/shm](https://img.shields.io/badge/L2-RAM_Backed-blue.svg)](#) [![DePIN: Telemetry Driven](https://img.shields.io/badge/DePIN-SQLite_WAL-green.svg)](#)

Sovereign Core OS is an autonomous, self-defending financial settlement hub that bridges physical Decentralized Physical Infrastructure Networks (DePIN) directly to native Bitcoin self-custody. By eliminating centralized custodians, trusted oracles, and honeypot cross-chain bridges, it transforms a localized Linux environment into an intent-based atomic swap router.

---

## 🏗️ The 3-Pronged Architecture

1. **L1 Base Layer (Autonomous Security):** BIP 199 Hash Time-Locked Contracts (HTLCs) secured by BIP 65 `OP_CHECKLOCKTIMEVERIFY`. Autonomous `OP_ELSE` refund paths guarantee zero-risk self-custody if counterparty routes fail.
2. **L2 Routing Layer (Bare-Metal Execution):** Zero-latency shared memory intent ring (`/dev/shm`) matching cross-chain swaps at RAM speed.
3. **L3 Intrinsic Valuation (DePIN Infrastructure):** Live bandwidth and node telemetry aggregated across 7 passive infrastructure applications (Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns.app, Honeygain, Docker Mysterium) stored in concurrent SQLite WAL ledgers.

---

## 🌐 Cross-Community Architectural Foundations

### 1. Bitcointalk.org (Base-Layer Cryptography)
* **Pioneering Atomic Swaps:** Direct implementation of Tier Nolan’s 2013 HTLC cross-chain swap model.
* **BIP 65 & BIP 199 Alignment:** Absolute block-height script anchoring avoiding Median-Past-Time (MPT) drift.
* **Fee Sniping & Griefing Protection:** Enforces asymmetric locktime deltas ($T_{hub} \ge 2 	imes T_{spoke}$) and BIP 125 RBF fee bumping to defeat mempool replacement attacks.

### 2. XDA Developers (Mobile & System Execution)
* **Headless Terminal Administration:** Custom zero-truncation buffer execution (`replace("
", chr(10))`) engineered for remote Termux SSH workflows.
* **Host Hardening:** UFW port 22 whitelisting, Fail2Ban intrusion prevention, and kernel AppArmor isolation (`apparmor=1`).

### 3. GitHub (Open Spoke Interoperability)
* **Open Spoke Standard (OSIS):** External chains (EVM, Solana, Move) connect via standardized intent structures without accessing classified core algorithms.
* **Community Extensibility:** Public interfaces for custom DePIN telemetry scrapers and terminal UI dashboards.

---

## 🛡️ Classified Core Boundaries (OPSEC Notice)

To preserve operational security and network defense, the proprietary mathematical engines (Null-State arithmetic, Fischer Random entropy, 3D spatial scaling) and active automated trade execution triggers remain **strictly classified** and air-gapped from public repositories. External contributors can develop against the public Spoke Specification (`docs/OPEN_SPOKE_SPEC.md`).

---

## 🤝 How to Build on Sovereign Core

* **Add a DePIN Scraper:** Implement new node monitors under `plugins/` with `#GoodFirstIssue`.
* **Deploy an External Spoke Vault:** Read [OPEN_SPOKE_SPEC.md](docs/OPEN_SPOKE_SPEC.md) to deploy an HTLC vault on your native blockchain.
* **Terminal Dashboards:** Build visual extensions consuming the local read-only loopback API at `127.0.0.1:8000`.

See [CREDITS.md](CREDITS.md) for full attribution across developer communities.
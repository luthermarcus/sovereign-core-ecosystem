# Sovereign Core OS (SOS v7.71.83-release)
### Decentralized, Relativistic, and Rootless Microkernel Ecosystem

[![Version](https://img.shields.io/badge/version-v7.71.83--release-blue.svg)](https://github.com/luthermarcus/sovereign-core-ecosystem)
[![Platform](https://img.shields.io/badge/platform-Android%2017%20Termux%20%7C%20Linux%20Mint-green.svg)](https://github.com/luthermarcus/sovereign-core-ecosystem)
[![Architecture](https://img.shields.io/badge/architecture-Rootless%20SELinux%20Harmony-brightgreen.svg)](https://github.com/luthermarcus/sovereign-core-ecosystem)
[![Ledger](https://img.shields.io/badge/ledger-AuxPoW%20Bitcoin%20L1%20%7C%20Rollup%20L2-orange.svg)](https://github.com/luthermarcus/sovereign-core-ecosystem)

Sovereign Core OS (SOS) is an invariant, trustless microkernel designed for resource-constrained, high-security mobile devices (Android Termux) and desktop workstations (Linux Mint). It combines relativistic physics-based telemetry pacing, deterministic multi-layer sidechain mining, and enclave-authenticated peer-to-peer data streaming into an autonomous, zero-drift ecosystem.

---

## 1. Architectural Foundations & Mathematical Primitives

### Relativistic Telemetry & Lorentz Horizon Gating
Network traffic accounting and database state flushes are governed by Minkowski 4D spacetime intervals:
$$\Delta s^2 = c^2\Delta t^2 - (\Delta x^2 + \Delta y^2 + \Delta z^2)$$

The dynamic Lorentz factor ($\gamma$) dictates relativistic rate damping and dynamic surge gas fees:
$$\gamma = rac{1}{\sqrt{1 - eta^2}}, \quad eta = rac{v}{c}$$

State commits to flash memory are damped by an invariant gate: updates trigger if and only if $\Delta t \ge 60	ext{s}$ AND $\Delta \gamma \ge 0.10$. Otherwise, the node preserves zero-commit equilibrium, preventing write amplification on mobile UFS flash.

### Multi-Layer Sidechain Mining & Three-Prong Execution
1. **Layer 1 (AuxPoW Anchor):** Merged-mining commitment (`fox://l1/auxpow/coinbase_44b`) binding an 18-chunk Merkle root into parent Bitcoin coinbase transactions via 80-byte serialized headers and proper-time nonces ($	au = 955	ext{s}$).
2. **Layer 2 (Relativistic Rollup VM):** Sub-second micro-royalties (85% Creator / 15% Seeder) governed by Lorentz gas pricing ($1.2503\%$).
3. **Three-Prong Execution Matrix:**
   * **Prong 1 (Memoized Dirty-Bit):** Skips disk writes and commits when zero state mutations occur.
   * **Prong 2 (Single-Process Autopilot):** Executes pulses in a single process, avoiding child-process termination under Android 17.
   * **Prong 3 (Savepoint Sandbox):** Quarantines untrusted or unverified hops within SQLite `SAVEPOINT` checkpoints.

### Bounded Softmax Mixture of Experts (MoE) Routing
Inspired by high-performance sparse MoE architectures (xAI/Grok), `bin/sos-grok-router` calculates route selection across layers using a thermally bounded softmax scaled by the Lorentz factor:
$$P(	ext{expert}_i) = rac{e^{z_i / \gamma}}{\sum_j e^{z_j / \gamma}}$$

---

## 2. Community Attributions & Upstream Standards

Sovereign Core OS directly credits and adheres to foundational research and engineering standards established by the open-source community:

* **Leslie Lamport (1978):** Distributed event ordering, causal clock synchronization, and logical clock primitives.
* **Albert Einstein (1905, 1915):** Special and General Relativity formulations ($\gamma$, proper time $	au$, Minkowski metrics) governing DePIN telemetry pacing and gas pricing.
* **Jason A. Donenfeld (zx2c4 / WireGuard):** Modern kernel and userspace cryptographic tunneling architecture.
* **Bram Cohen & BitTorrent Community:** BEP-52 compact binary bitfield piece negotiation architecture.
* **topjohnwu & osm0sis (XDA Developers):** Android systemless interface research, mount namespace isolation, and rootless compatibility shims.
* **xAI / Grok Open-Source Community:** Sparse Top-2 Mixture of Experts (MoE) routing, vector bitmasks, and stable bounded softmax formulations.
* **Mysterium Network & P2Pool Node Operators:** Traffic volume accounting, WAL truncation caps, pool-hopping resistance, and mobile battery conservation.

---

## 3. Node Operator Policy & Anti-Abuse Standards

To ensure fair bandwidth distribution across decentralized mesh networks, nodes enforce strict anti-abuse rules via `bin/sos-anti-abuse`:

* **Zero-Satoshi Leeching:** P2P chunk requests must supply an enclave HMAC signature verifying a valid payment split (85% Creator / 15% Seeder). Unsettled requests are rejected.
* **Sybil Request Flooding:** Peers exceeding 500 bitfield requests per minute without corresponding chunk downloads are rate-limited.
* **Malformed Handshake Penalties:** Peers with an authentication error rate exceeding 30% are quarantined (`sos_peer_quarantine`) to prevent resource exhaustion.
* **Strict Rootless Purity:** The node operates entirely unprivileged within Android SELinux user-space. Superuser (`su`) privileges are neither requested nor required, preserving system integrity and hardware attestation.
* **Process Stability:** Node operators on Android 14+ must enable:
  $$\text{Settings} \longrightarrow \text{System} \longrightarrow \text{Developer Options} \longrightarrow \textbf{"Disable child process restrictions"}$$

---

## 4. Quickstart & Command Interface

### Primary Applets (`bin/`)
| Applet | Description |
| :--- | :--- |
| `sos --status` | Display full microkernel health, L1/L2 endpoints, and safety flags. |
| `sos-top` | Real-time single-screen terminal dashboard. |
| `sos-audit` | Complete 6-pillar system and ledger integrity verification. |
| `sos-pulse` | Autonomous single-word autopilot sync and equilibrium anchor. |
| `sos-router` | Deterministic layer router (L1 AuxPoW / L2 VM / L3 Sandbox). |
| `sos-grok-router` | Grok-inspired Top-2 sparse MoE gating router. |
| `sos-bitfield-sync` | BEP-52 compact binary bitfield piece negotiator. |
| `sos-mesh-swarm` | Peer ping and socket reachability engine. |
| `sos-anti-abuse` | Peer fair-share traffic sentinel and quarantine manager. |
| `sos-rootless-guard` | SELinux user-space purity and permission validator. |
| `sos-mod-probe` | Python 3.14 standard library and C-API dependency auditor. |

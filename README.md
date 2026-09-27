# Sovereign Core OS (`v6.27.0-beta`)
*Modular Edge-Node Telemetry, Resource Management & Sandbox Ecosystem*

---

## 1. Project Overview & Architectural Scope
Sovereign Core OS is an independent, modular research and resource-management environment engineered for Linux-based host systems (`luther-Inspiron-1525`). 

> **Community Alignment & Scope Note:** 
> This project operates strictly as an out-of-process, modular execution layer and local telemetry dashboard. It does not propose, modify, or enforce base-layer consensus rules, protocol changes, or mainnet soft forks. All experimental cross-chain telemetry, yield indexing, and resource management modules are decoupled and executed entirely within local sandboxed partitions (`/dev/shm`) to maintain absolute separation from base-layer network mechanics.

---

## 2. Development Roadmap & Milestones

*   **Phase 1: Foundation & Telemetry Core (Completed)**
    *   Establishment of Layer 1 host security hardening (UFW, AppArmor, hardware thermals via `i8kutils`)[span_1](start_span)[span_1](end_span).
    *   Deployment of SQLite Write-Ahead Logging (WAL) for persistent metrics (`l1_warden.db`, `ecosystem_metrics.db`).
*   **Phase 2: Modular Multi-Display & TUI Interface (Completed)**
    *   Implementation of the 6-display startup greeting engine (`greet`).
    *   Development of the 4-page interactive master TUI (`sos`) with single-digit numeric routing.
*   **Phase 3: Automated Lifecycle & Yield Optimization (Active - `v6.27.0-beta` Fault-Tolerant Release)**
    *   Integration of automated background telemetry crons (`ecosystem_cron.py`).
    *   Simulation of modular auto-compounding yield mechanisms within local AMM liquidity partitions.
*   **Phase 4: Advanced Sandboxing & Diagnostic Auditing (Planned)**
    *   Expansion of Automated Incident Response (AIR) diagnostic triggers.
    *   Refinement of decoupled JSON ledger routing (`ecosystem_config.json`) to ensure zero mobile SSH paste friction.

---

## 3. Core Modules & Usage
- **`greet`**: Instant multi-display status rendering.
- **`sos`**: Interactive multi-page master dashboard TUI.
- **Direct CLI Flags**: 
  - `sos --depin`: DePIN portfolio and yield metrics audit[span_2](start_span)[span_2](end_span).
  - `sos --wallet`: Local liquidity and reserve tracking.
  - `sos --kernel`: Host and sandbox integration audit[span_3](start_span)[span_3](end_span).

# Sovereign Core OS (`v3.4.0-beta`)
*Bare-Metal DePIN Microkernel, Tri-Layer Architecture & SC-GPL Capital Protocol*

---

## 1. DePIN Infrastructure & Node Operators
- **Hardware Architecture:** Optimized for commodity x86_64 systems (e.g., Dell Inspiron 1525).
- **Privacy Consensus:** Zero open clearnet ports. Autonomous routing enforced via Tor SOCKS5 loopback (`127.0.0.1:9050`) and Tor v3 Hidden Services (port 8181).
- **Resource Management:** RAM telemetry via `/dev/shm`, atomic SQLite WAL ledgers (`0o664`), and Google BBR TCP congestion tuning.

## 2. Core Blockchain, Two-Way Pegs & Developer Royalties
- **Tri-Layer Modular Sidechain Engine:**
  - **Layer 1 (Alpha):** DePIN node routing and hardware state verification.
  - **Layer 2 (Beta):** Native FOX financial settlement and 2-way peg with Bitcoin.
  - **Layer 3 (Gamma):** Client-Side Logic Virtualization (BitVM paradigm). Arbitrary logic executes off-chain, producing SHA-256 state roots anchored to Layer 2.
- **The SC-GPL Consensus Standard:** AMM routers automatically divert 5% of gross swap volume to the Developer Treasury Vault, replacing predatory token pre-mines with sustainable protocol monetization.
- **Cryptographic License Vaults:** Protects developer intellectual property using HMAC-SHA256 commitment schemes, ensuring open verification without exposing proprietary heuristics.

## 3. Hardware Modding & Administration (XDA)
- **Termux & Android Integration:** Remote terminal management optimized for mobile SSH clients with active TCP keepalive pulses (`ServerAliveInterval 30`).
- **Buffer Integrity:** Terminal line discipline enforced via raw `termios` single-keystroke listeners to eradicate terminal bleed.

## 4. Community Attributions
- **Bitcoin Core / Bitcointalk:** For BIP 300 Drivechain architecture, 2-way peg mechanisms, and client-side validation philosophies.
- **XDA Developers:** For bare-metal hardware modding and Linux namespace isolation.

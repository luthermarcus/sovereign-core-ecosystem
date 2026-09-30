# 🦊 Sovereign Core OS (SOS)
**A Decentralized, Hardware-Agnostic Operating System & AuxPoW Blockchain**
Sovereign Core OS (SOS) unifies passive bandwidth generation (DePIN), quantum-resistant consensus, and rootless L2 sandboxing into a single lightweight terminal interface. Designed to run seamlessly on Linux hosts and mobile edge nodes (via Termux/Shizuku).
## 🏛 Ecosystem Architecture
* **Zero-Latency IPC:** Eliminates REST APIs in favor of volatile RAM buses (/dev/shm SQLite WAL ledgers).
* **Dual-Valuation Tokenomics:** The native 0xFOX token is backed by Protocol-Owned Liquidity (POL) generated via 7 integrated DePIN applications.
* **Bitcoin-Pegged L1 Consensus:** Secures the ledger using Merged Mining (AuxPoW), injecting a 44-byte marker directly into the parent chains coinbase scriptSig.
* **Boomerang Escrow:** Utilizes causal time windows for trustless cross-chain liquidity routing.
## 🛡 Regression Prevention
1. **The Box Ideology:** All TUI wallets must use interactive curses.box() dialogs. View-only wallets are prohibited.
2. **Dynamic Module Booting:** core_router.py must physically execute orphaned scripts via subprocess.Popen.
3. **Strict AppArmor Sandboxing:** All background daemons must be bound to the /etc/apparmor.d/sovereign-ecosystem profile.

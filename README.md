# 🦊 Sovereign Core OS (OSIS) & FOX Bridge
Version: v7.71.24-beta | Consensus: AuxPoW (Merged Mining)
L1/L2 DePIN node harmonizing AuxPoW with intent liquidity pools.

## 🌟 Sandbox & Tokenomics
* **Virtualization:** Wallet and routing isolated from core consensus daemons.
* **Dual-Valuation FOX:** Utility (DePIN bandwidth) & DEX/CEX Protocol-Owned Liquidity.
* **Interoperability Bridge:** Flag-pulling error handling & intent routing (Δt) eliminate double-spending.

## 🏛️ Architecture & Telemetry
* **Consensus:** Bitcoin-pegged AuxPoW.
* **Daemons:** core_router.py & node_manager.py govern thermal loads.
* **Telemetry:** 7 apps (Native/Docker Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns.app, Honeygain) synced to `/dev/shm` SQLite WAL ledgers.
* **OS Hardening:** `vm.swappiness=10`, UFW, Fail2Ban, Fischer Random (960) entropy.

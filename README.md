# Sovereign Core OS (`v3.8.0-beta`)

## 1. Hardware Warden & Proof of Useful Work (PoUW)
Addressing critical hardware wear and energy waste:
- **L1 Hardware Warden:** Actively monitors bare-metal thermals and SSD wear vectors. If CPU/NVMe controllers approach XDA's 75°C throttling limit, the Warden dynamically chokes L2 compute.
- **L2 PoUW Miner:** Replaces useless SHA-256 hashing with Proof of Useful Work. Nodes validate DePIN network routing and AMM liquidity reserves, generating value without melting commodity laptop hardware.
- **SSD Protection:** State transitions and telemetry rollups are written exclusively to `/dev/shm` (RAM cache), bypassing the SSD NAND flash entirely to preserve hardware lifespans.

## 2. Decentralized Governance & Tri-Layer Architecture
- **Bitcointalk Ideology:** Zero-trust privacy, BIP 300 Drivechains, and non-custodial bridging.
- **DeFi Interoperability:** SC-GPL AMM capital raise protocol diverts 5% liquidity fees natively to developers.

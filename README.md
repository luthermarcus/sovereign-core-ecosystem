# 🦊 Sovereign Core OS: Decentralized DePIN Settlement Hub

[![Bitcoin: L1 HTLC](https://img.shields.io/badge/Bitcoin-L1_BIP199-orange.svg)](#) [![ERC-7683: Ready](https://img.shields.io/badge/ERC--7683-Cross_Chain_Intents-blue.svg)](#) [![Protocol Fee: 5%](https://img.shields.io/badge/Fee-500_BPS_Treasury-green.svg)](#)

Sovereign Core OS is an autonomous settlement hub bridging physical DePIN node bandwidth directly to Bitcoin self-custody.

## 🚀 Mainnet Operational Roadmap (Hybrid Architecture)
To guarantee 100% uptime on constrained hardware while expanding cross-chain interoperability, Sovereign Core utilizes a **Dual Bitcoin L1 Backend**:

1. **Primary: Pruned Bitcoin Core (`bitcoind -prune=1000`)**
   - **Role:** Absolute self-sovereignty and full consensus validation. 
   - **Mechanics:** The local daemon uses `createrawtransaction` to autonomously split incoming UTXOs into a 95% BIP-199 settlement output and the 5% protocol treasury output.
2. **Fallback: Electrum SPV Daemon**
   - **Role:** Ultra-lightweight failover. If the host machine thermal throttles during block processing, the router seamlessly drops to decentralized Electrum SPV indexing. This ensures external spoke pools never experience execution timeouts.

## 🌐 The ERC-7683 Intent Solver Network
The Hub acts as a trustless intent solver. External EVM liquidity pools (Ethereum, Polygon, Arbitrum) broadcast standardized **ERC-7683 cross-chain intents**. Our `/dev/shm` RAM router ingests these intents, prices them against intrinsic DePIN physical throughput (Mysterium, EarnApp, TraffMonetizer), and settles them autonomously via the hybrid Bitcoin backend.

## 💎 On-Chain 5% Capital Generation
A fixed 5% protocol fee is evaluated on every atomic swap to continuously build community capital:
- **2.5% Community Treasury & Developer Grant Fund**
- **2.5% Physical Node Infrastructure Pool**

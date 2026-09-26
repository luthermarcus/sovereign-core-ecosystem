# Sovereign Core OS Ecosystem (v2.25.0-master)

## Production Master Architecture & Yield Auto-Compounding
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **AMM Smart Contract Engine (`amm_smart_contract.py`):** Inspired by DeFi yield aggregators, this module autonomously sweeps the 5% SC-GPL Treasury tax into the FOX and PARROT SQLite DEX pools. It utilizes the Constant Product Formula to algorithmically balance internal token prices without EVM bloat.
- **Autonomous P2P Tor Sync:** The background `dex_daemon.py` autonomously pings known `.onion` addresses to maintain DEX synchronization.
- **Pure DePIN Infrastructure:** Exclusively orchestrates decentralized routing (Mysterium) and off-chain liquidity pools.

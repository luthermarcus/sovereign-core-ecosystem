# Sovereign Core OS Ecosystem (v2.21.0-master)

## Production Master Architecture & Automated Infrastructure
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **Interactive DEX Diagnostics:** Use `python3 ecosystem_dashboard.py --ping-dex` to verify Tor socket bridge responsiveness locally.
- **Active DEX Daemon (`dex_daemon.py`):** An asynchronous Python socket server bound to the local Tor Hidden Service port, actively listening for peer liquidity requests.
- **Tor v3 Native P2P DEX Gossip:** Dynamically generated cryptographic `.onion` hostnames for true off-chain SQLite data swaps.
- **SC-GPL Economic Consensus:** Mandates a 5% allocation of node routing yield to the Global Liquidity Treasury and a 0.05% DEX transaction fee to hardware miners.
- **Pure DePIN Infrastructure:** Exclusively orchestrates decentralized routing (Mysterium) and off-chain liquidity pools.
- **BIP44 HD Self-Custody:** Key derivation strictly bound to path `m/44'/0'/0'/0/0`.

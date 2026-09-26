# Sovereign Core OS Ecosystem (v2.15.0-master)

## Production Master Architecture & SC-GPL Consensus
- **Repository:** [GitHub - luthermarcus/sovereign-core-ecosystem](https://github.com/luthermarcus/sovereign-core-ecosystem)
- **SC-GPL Economic Consensus:** Mandates a 5% allocation of node routing yield to the Global Liquidity Treasury and a 0.05% DEX transaction fee to hardware miners.
- **Pure DePIN Infrastructure:** Exclusively orchestrates decentralized nodes (native and containerized Mysterium routing) and off-chain liquidity pools (FOX/BTC, PARROT/BTC). Centralized proxy applications are purged.
- **BIP44 HD Self-Custody:** Key derivation bound to path `m/44'/0'/0'/0/0` in encrypted SQLite WAL ledgers.
- **Zero-Trust Network:** Full network isolation using local Tor SOCKS5 loopbacks (`127.0.0.1:9050`).
- **AI-Assisted Development:** Built-in `.github/copilot-instructions.md` configuration keeps external and AI contributors aligned with project mandates.

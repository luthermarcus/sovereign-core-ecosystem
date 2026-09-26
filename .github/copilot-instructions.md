# Sovereign Core OS - AI Developer Instructions

When generating, refactoring, or analyzing code in this repository, strictly adhere to the following architectural mandates:

1. **Pure DePIN Infrastructure:** Never suggest or integrate centralized proxy applications (e.g., EarnApp, Honeygain, TraffMonetizer). Only integrate true Decentralized Physical Infrastructure Networks (DePIN) like Mysterium node routing.
2. **Blockchain Interoperability:** All cryptographic key management MUST utilize BIP44 Hierarchical Deterministic (HD) derivation paths (specifically m/44'/0'/0'/0/0).
3. **Database Architecture:** All databases must use SQLite with Write-Ahead Logging (PRAGMA journal_mode=WAL) and strict 0o664 permissions.
4. **Zero-Trust Network:** All external network requests must route through a local Tor SOCKS5 proxy (127.0.0.1:9050). No open inbound clearnet ports.
5. **Consensus Royalties:** All derivative works and node operations must respect the SC-GPL consensus rules: 5% DePIN yield allocation to the Liquidity Treasury and 0.05% DEX swap fees to node miners.

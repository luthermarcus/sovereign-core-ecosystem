# Sovereign Core OS - AI Developer Instructions

1. **Pure DePIN Infrastructure:** Never integrate centralized proxy applications. Only integrate true Decentralized Physical Infrastructure Networks (DePIN) like Mysterium routing.
2. **Blockchain Interoperability:** Cryptographic key management MUST utilize BIP44 Hierarchical Deterministic (HD) derivation paths (m/44'/0'/0'/0/0).
3. **Database Architecture:** All databases must use SQLite with Write-Ahead Logging (PRAGMA journal_mode=WAL) and strict 0o664 permissions.
4. **Zero-Trust Network:** All external network requests must route through a local Tor SOCKS5 proxy (127.0.0.1:9050). No open inbound clearnet ports.
5. **Consensus Royalties:** All derivative works must respect the SC-GPL rules: 5% DePIN yield allocation to the Liquidity Treasury and 0.05% DEX swap fees to node miners.

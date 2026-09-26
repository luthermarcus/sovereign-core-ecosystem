# Sovereign Core OS (`v2.7.0-beta`)
*Bare-Metal DePIN Microkernel, Cross-Chain AMM Engine & Developer Capital Protocol*

---

## 1. Documentation for DePIN Node Operators
- **Host System Compatibility:** Bare-metal Linux Mint / Ubuntu LTS installations. Optimized for commodity hardware (e.g. Dell Inspiron 1525).
- **Network Isolation:** Operates zero open clearnet ports. Outbound routing enforced via local Tor SOCKS5 loopback (`127.0.0.1:9050`) and onion hidden services on port 8181.
- **Resource Management:** Real-time RAM-backed caching via `/dev/shm`, atomic SQLite WAL database ledgers, and zero-cost sysctl Google BBR TCP congestion optimization.
- **Node Matrix:** Aggregates passive yield metrics across native Mysterium node protocols and unprivileged diagnostic scrapers.

## 2. Documentation for Blockchain & DEX Developers
- **The SC-GPL Developer Capital Raise Standard:** Replaces predatory token pre-mines with protocol-level fee diversion. The off-chain AMM smart contract router diverts exactly 5% of all swap volume into registered Developer Treasury Vaults:
  $$\Delta x_{\text{net}} = \Delta x \times (1 - 0.05)$$
- **Multi-Chain Wallet Interoperability:** Implements standardized BIP44 hierarchical deterministic derivation across:
  - **Bitcoin (BTC):** `m/44'/0'/0'/0/0` (Taproot / UTXO)
  - **Ethereum (ETH):** `m/44'/60'/0'/0/0` (EVM Account Model)
  - **BNB Chain (BNB):** `m/44'/714'/0'/0/0` (PoSA EVM)
  - **Tron (TRX):** `m/44'/195'/0'/0/0` (Base58 / Energy Model)
  - **Native FOX:** L2 Two-Way Pegged Settlement Asset
- **Constant Product AMM Engine:** Off-chain smart contracts executing constant invariant verification ($x \times y = k$) across `FOX/USDC`, `FOX/BTC`, `FOX/ETH`, `FOX/BNB`, and `FOX/TRX`.

## 3. Documentation for Bare-Metal & Hardware Modders (XDA)
- **Termux & Mobile SSH Tunneling:** Hardened remote administration via Android Termux with persistent TCP keepalive pulses (`ServerAliveInterval 30`).
- **Process Hierarchy:** Clean decoupling of non-blocking host HUD greeting sequences from the interactive 5-page Sovereign Core Virtual OS Sandbox (`sos`).
- **Buffer Integrity:** Terminal line discipline managed via `termios` and `tty.setraw` instant keystroke event listeners, eliminating standard input bleed.

# Sovereign Core OS (`v5.0.0-beta`)

## 1. Decentralized Immune System & Fork Defense
Addressing the vulnerabilities exposed by the Steem/Hive takeover and Uniswap Vampire Attacks:
- **Tri-Faction Governance:** Network expansions and consensus changes require approval from Bitcointalk, XDA, and DeFi communities.
- **Cryptographic Licensing:** Proprietary heuristics are protected via HMAC-SHA256 commitments. The code is public; the execution variables are shielded.
- **Protocol-Owned Liquidity (POL):** Replaces mercenary LPs with an autonomous 5% fee that permanently locks FOX inside the community treasury.

## 2. Infrastructure
- **L1/L2 Separation:** Hardware thermals and firewall routing are locked to `l1_warden.db`. High-frequency DePIN validations occur in RAM and commit to `l2_rollup.db`.
- **BIP 301 Blind Merged Mining:** The L1 Host natively hashes L2 state roots via `/dev/shm`, unifying the ecosystem without L1 bloat.

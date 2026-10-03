# 🏛️ Sovereign Core OS — Safe-DEX & Anti-Honeypot Standards

Decentralized exchanges frequently suffer from malicious token listings (honeypots, unrenounced mints, and sudden liquidity withdrawals). Sovereign Core enforces mathematical invariants on all multi-chain pairs.

---

## 🛡️ Anti-Shitcoin Verification Manifest

Before any token can pair with Bitcoin L2 or FOX via Project Boomerang, it must satisfy four immutable criteria:

| Invariant Requirement | Standard Threshold | Failure Consequence |
| :--- | :--- | :--- |
| **Max Transaction Tax** | $\le 1.0\%$ Buy / $\le 2.0\%$ Sell | Route permanently blacklisted (`EXCESSIVE_TAX`). |
| **Minting Authority** | Completely renounced or locked in 4-of-7 multisig | Rejected (`UNRENOUNCED_SUPPLY_RISK`). |
| **Liquidity Lock Duration** | $\ge 90\text{ days}$ non-custodial timelock | Rejected (`UNLOCKED_RUG_RISK`). |
| **Pre-Flight Sandbox Trace** | Verified buy, approve, and sell sequence in PRoot EVM sandbox | Rejected (`SIMULATED_HONEYPOT`). |

---

## 🪃 The Boomerang Auto-Refund Mechanism

All cross-chain routes leverage bilateral Hash Time Locked Contracts (HTLCs).
* **Guaranteed Delivery**: If the destination network settles, funds transfer atomically.
* **Guaranteed Rebound**: If a bridge peer stalls, goes offline, or attempts an invalid state commit, the locktime automatically expires after 144 blocks, rebounding 100% of deposited capital back to the sender's origin wallet.

---

## 💰 P2Pool Fee Distribution Formula

For every settled swap, a 0.25% protocol fee is allocated as follows:
* **80% — Liquidity Providers**: Distributed proportionally to committed capital.
* **15% — Sovereign Edge Relayers**: Compensates active nodes (Pixel 10 Pro XL / Dell Inspiron hosts) for bandwidth and state validation.
* **5% — Sovereign Improvement Proposal (SIP) Reserve**: Funds peer-reviewed bug fixes and mathematical audits.

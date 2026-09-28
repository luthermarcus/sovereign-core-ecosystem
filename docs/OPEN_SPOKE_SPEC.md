# 🦊 Open Spoke Interoperability Standard (OSIS)
## Specification Version: 2.2.0

## 1. Architectural Model
Sovereign Core OS operates as a trustless Settlement Hub. External blockchains operate as Independent Spokes. Spoke communities manage their own collateral pools and user interfaces, eliminating centralized honeypots.

## 2. Cryptographic Intent Parameters
External spoke vaults must construct cross-chain swap intents meeting the following criteria:

### A. Hashlock Clause (Payment Path)
* **Algorithm:** Raw SHA-256 (`OP_SHA256`).
* **Push Prefix:** Standard `0x20` (32 bytes).
* **Preimage Length:** Exactly 32 bytes (256 bits).

### B. Timelock Clause (Safety Boomerang)
* **Opcode:** `OP_CHECKLOCKTIMEVERIFY` (CLTV).
* **Push Prefix:** `0x04` (4 bytes little-endian integer).
* **Threshold Format:** Absolute Block Height (integers < 500,000,000). UNIX timestamps are strictly prohibited to eliminate Median-Past-Time (MPT) drift.
* **Asymmetric Safety Delta:** Hub locktime ($T_{hub}$) must satisfy:
  $$T_{hub} \ge 2 \times T_{spoke}$$

### C. Fee Protection
* **Signaling:** All on-chain broadcasts must signal BIP 125 Replace-By-Fee (RBF) to permit dynamic fee escalation.

## 3. Intrinsic Valuation Calculation
The Hub calculates exchange rates via physical throughput rather than external oracles:
$$V_{rate} = \frac{\sum (\text{Bandwidth}_{GB} \times \text{Yield}_{USD})}{\text{Active Nodes}}$$
External spokes can query this live intrinsic metric via the Hub’s loopback API at `/api/depin/valuation`.

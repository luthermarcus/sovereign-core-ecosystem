# 🦊 Open Spoke Interoperability Standard (OSIS)
## Specification Version: 2.3.0

## 1. Architectural Model
Sovereign Core OS operates as a trustless Settlement Hub. External blockchains operate as Independent Spokes. Spoke communities manage their own collateral pools and user interfaces, eliminating centralized honeypots.

## 2. Cryptographic Intent Parameters
External spoke vaults must construct cross-chain swap intents meeting the following criteria:

### A. Hashlock Clause (Payment Path)
* **Algorithm:** Raw SHA-256 (`OP_SHA256`).
* **Push Prefix:** Standard `0x20` (32 bytes).
* **Preimage Length:** Exactly 32 bytes (256 bits).
* **Verification:** The preimage must be exposed on-chain by the claiming party to claim the funds.

### B. Timelock Clause (Safety Boomerang)
* **Opcode:** `OP_CHECKLOCKTIMEVERIFY` (CLTV).
* **Push Prefix:** `0x04` (4 bytes Little-Endian integer).
* **Threshold Format:** Absolute Block Height (integers < 500,000,000). UNIX timestamps are strictly prohibited to eliminate Median-Past-Time (MPT) drift.
* **Asymmetric Safety Delta:** Hub locktime ($T_{hub}$) must satisfy:
  $$T_{hub} \ge 2 \times T_{spoke}$$

### C. Fee Protection
* **Signaling:** All on-chain broadcasts must signal BIP 125 Replace-By-Fee (RBF) to permit dynamic fee escalation.

## 3. Verifiable Intrinsic Valuation Calculation
The Hub calculates exchange rates via physical QoS-weighted throughput:
$$V_{QoS} = \sum \left( \text{Yield}_i \times \frac{\text{Uptime}_i}{100} \times \left(1 - \frac{\text{Latency}_i}{1000}\right) \right)$$
Spokes can audit the verifiable proof-of-yield hash chain at `/api/depin/valuation`.

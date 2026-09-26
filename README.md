# Sovereign Core OS (`v6.0.0-beta`)
*Dynamic Role-Switching, DePIN Telemetry Emulation, L1/L2 Security & XDA AIR*

## 1. Built-in Role-Switching Dashboard
To facilitate rigorous beta testing across all system layers:
- **Instant Role Migration:** Seamlessly switch between **L1 Bare-Metal Miner**, **L2 Sandbox Tester**, and **XDA Auditor** profiles without restarting services or encountering syntax errors.
- **Ledger-Driven State:** Role states are managed atomically via `ecosystem_config.json`, keeping shell execution clean and robust.

## 2. DePIN Telemetry Emulation & Decentralization
- **6-App Passive Income Integration:** Actively tracks Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns.app, and Honeygain earnings securely in RAM (`/dev/shm`).
- **Verifiable Proofs:** Converts centralized node metrics into zero-trust cryptographic state roots anchored directly to the L1 basechain.

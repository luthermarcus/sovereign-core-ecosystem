# Sovereign Core OS (`v5.5.0-beta`)
*Dual-Path Transaction Guard, Anti-Phishing Emulation & L1/L2 Hardware Warden*

## 1. Dual-Path Security & Phishing Defense
To protect users from fake dApps, wallet drainers, and malicious signature prompts:
- **Side A (Test Sandbox Channel):** Intercepts all incoming connection requests and runs a dry-run emulation in RAM (`/dev/shm`) to inspect bytecode and permissions.
- **Side B (Official Settlement Channel):** Only establishes an official connection and commits state anchors after Side A certifies zero-risk execution.
- **Hardware Isolation:** L1 Host basechain ledgers (`l1_warden.db`) remain strictly partitioned from user-space network interactions.

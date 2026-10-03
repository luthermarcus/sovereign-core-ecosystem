# Sovereign Core OS — Multi-Machine Credential & Node Topology

## Machine Credential Registry
1. **Primary Mobile Workstation (Foxy Node — Google Pixel 10 Pro XL)**:
   - Environment: Termux Host + PRoot Debian Enclave
   - SSH Key Pair: `Pixel-Sovereign-Node-2026` (Ed25519)
   - GitHub Access Token: `Pixel-Sovereign-Core-2026` / `Pixel-Sovereign-Node-2026` (repo-scoped)
   - Role: Real-time telemetry, 5-tab TUI workstation, Boomerang AMM executor.

2. **Secondary Core Node (Dell Inspiron 1525 / Ubuntu / Linux Mint)**:
   - Environment: Standalone Linux Native Workstation
   - Role: Native Mysterium node, Docker container fleet backup, secondary WAL sync.
   - Access: Isolated key-based SSH with UFW port 22 whitelisting.

## Zero-Leak DLP Security Boundary
* Private keys, tokens, and raw credentials MUST NEVER be hardcoded into `.py` or committed to Git.
* Enforced via `.git/hooks/pre-commit` and `sos-dlp-guard` fail-closed pattern matching.

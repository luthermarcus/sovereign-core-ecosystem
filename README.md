# Sovereign Core OS (SOS v7.71.100-beta)

Rootless, deterministic Python 3.14 standard-library microkernel ecosystem running on Android Termux (pixel-sovereign, aarch64, Android 17 SDK 37) and Linux Mint workstations.

## Constitutional Invariants & Architecture
- **Privilege Sandbox**: `STRICT_ROOTLESS_PURITY` (`u0_a413`, zero root/su, SELinux user-space isolation)
- **Toolchain**: Python 3.14 Native Standard Library Only (`sqlite3`, `http.server`, `hashlib`, `ast`)
- **Verified Microkernel Applets**: 50 Rootless Standard-Library Executables
- **Anti-Hallucination Guard**: `sos-truth` (Real `ast.parse()` syntax verification + full 64-hex SHA-256 Merkle digest)

## Master Roadmap Status
| Milestone Range | Subsystem Architecture | Status |
| :--- | :--- | :--- |
| **Steps 01-68** | L1 AuxPoW / L2 Rollup VM & Triple-Entry Ledger | `ACTIVE` |
| **Steps 69-70** | Grok Sparse MoE Router & Telemetry Bridge | `ACTIVE` |
| **Steps 71-78** | Anti-Abuse Sentinel, Nilometer Relief & Jubilee Reset | `ACTIVE` |
| **Steps 79-80** | Claude Bridge & Cross-Community Skill Hub | `ACTIVE` |
| **Steps 81-95** | WireGuard Mesh Gateway, Onion Routing & DePIN Swarm | `ACTIVE` |
| **Steps 96-113** | Full 64-Hex SHA-256 Merkle Guard, Joined Ledger & FTS5 API | `ACTIVE` |

## Registered Microkernel Applets (50)
```text
01. sos-anti-abuse               -> [VERIFIED_ROOTLESS_STDLIB]
02. sos-audit                    -> [VERIFIED_ROOTLESS_STDLIB]
03. sos-auxpow-attestation       -> [VERIFIED_ROOTLESS_STDLIB]
04. sos-bandwidth-shaper         -> [VERIFIED_ROOTLESS_STDLIB]
05. sos-bitfield-sync            -> [VERIFIED_ROOTLESS_STDLIB]
06. sos-chain-bridge             -> [VERIFIED_ROOTLESS_STDLIB]
07. sos-claude-bridge            -> [VERIFIED_ROOTLESS_STDLIB]
08. sos-consensus                -> [VERIFIED_ROOTLESS_STDLIB]
09. sos-constitution             -> [VERIFIED_ROOTLESS_STDLIB]
10. sos-cron-sweep               -> [VERIFIED_ROOTLESS_STDLIB]
11. sos-dex                      -> [VERIFIED_ROOTLESS_STDLIB]
12. sos-faucet-epochs            -> [VERIFIED_ROOTLESS_STDLIB]
13. sos-grok-bridge              -> [VERIFIED_ROOTLESS_STDLIB]
14. sos-grok-router              -> [VERIFIED_ROOTLESS_STDLIB]
15. sos-heartbeat                -> [VERIFIED_ROOTLESS_STDLIB]
16. sos-input-sanitizer          -> [VERIFIED_ROOTLESS_STDLIB]
17. sos-ledger-audit             -> [VERIFIED_ROOTLESS_STDLIB]
18. sos-log-rotate               -> [VERIFIED_ROOTLESS_STDLIB]
19. sos-mesh-daemon              -> [VERIFIED_ROOTLESS_STDLIB]
20. sos-mesh-gateway             -> [VERIFIED_ROOTLESS_STDLIB]
21. sos-mesh-stream              -> [VERIFIED_ROOTLESS_STDLIB]
22. sos-mesh-swarm               -> [VERIFIED_ROOTLESS_STDLIB]
23. sos-mint-sync                -> [VERIFIED_ROOTLESS_STDLIB]
24. sos-mod-probe                -> [VERIFIED_ROOTLESS_STDLIB]
25. sos-nat-punch                -> [VERIFIED_ROOTLESS_STDLIB]
26. sos-net-inspect              -> [VERIFIED_ROOTLESS_STDLIB]
27. sos-network-diag             -> [VERIFIED_ROOTLESS_STDLIB]
28. sos-nilometer-jubilee        -> [VERIFIED_ROOTLESS_STDLIB]
29. sos-nostr-mesh               -> [VERIFIED_ROOTLESS_STDLIB]
30. sos-nostr-signaler           -> [VERIFIED_ROOTLESS_STDLIB]
31. sos-ns                       -> [VERIFIED_ROOTLESS_STDLIB]
32. sos-onion-route              -> [VERIFIED_ROOTLESS_STDLIB]
33. sos-pulse                    -> [VERIFIED_ROOTLESS_STDLIB]
34. sos-roadmap-sync             -> [VERIFIED_ROOTLESS_STDLIB]
35. sos-rootless-guard           -> [VERIFIED_ROOTLESS_STDLIB]
36. sos-router                   -> [VERIFIED_ROOTLESS_STDLIB]
37. sos-savepoint                -> [VERIFIED_ROOTLESS_STDLIB]
38. sos-skill-hub                -> [VERIFIED_ROOTLESS_STDLIB]
39. sos-state-proofs             -> [VERIFIED_ROOTLESS_STDLIB]
40. sos-threat-sentinel          -> [VERIFIED_ROOTLESS_STDLIB]
41. sos-top                      -> [VERIFIED_ROOTLESS_STDLIB]
42. sos-truth                    -> [VERIFIED_ROOTLESS_STDLIB]
43. sos-vault                    -> [VERIFIED_ROOTLESS_STDLIB]
44. sos-wal-sync                 -> [VERIFIED_ROOTLESS_STDLIB]
45. sos-watchdog                 -> [VERIFIED_ROOTLESS_STDLIB]
46. sos-web-bridge               -> [VERIFIED_ROOTLESS_STDLIB]
47. sos-wireguard-tunnel         -> [VERIFIED_ROOTLESS_STDLIB]
48. sos-zk-verify                -> [VERIFIED_ROOTLESS_STDLIB]
49. ssh-ed25519                  -> [VERIFIED_ROOTLESS_STDLIB]
50. termux-clipboard-set         -> [VERIFIED_ROOTLESS_STDLIB]
```

## Web Telemetry & SQLite Enclave Endpoints (127.0.0.1:8080)
- `GET /api/telemetry` : Live Lorentz Gamma, Proper Time (tau), Mesh Gateways & 64-hex SHA-256 Merkle Root
- `GET /api/audit` : SQLite WAL journal state, PRAGMA quick_check & 26-table row inventory
- `GET /api/ledger` : PRAGMA table_info schema introspection & SQL LEFT JOIN provenance across UTXO, Royalty & FTS5 tables
- `GET /api/search?q=...` : Parameterized SQLite FTS5 full-text search over sos_knowledge_fts

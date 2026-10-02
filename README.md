# Sovereign Core OS (SOS v7.71.100-beta)

Rootless, deterministic Python 3.14 standard-library microkernel ecosystem running on Android Termux (pixel-sovereign, aarch64, Android 17 SDK 37) and Linux Mint workstations.

## Constitutional Invariants & Architecture
- **Privilege Sandbox**: `STRICT_ROOTLESS_PURITY` (`u0_a413`, zero root/su, SELinux user-space isolation)
- **Toolchain**: Python 3.14 Native Standard Library Only (`sqlite3`, `http.server`, `hashlib`, `ast`)
- **Verified Microkernel Applets**: 73 Rootless Standard-Library Executables
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

## Registered Microkernel Applets (73)
```text
01. sos-anti-abuse               -> [VERIFIED_ROOTLESS_STDLIB]
02. sos-audit                    -> [VERIFIED_ROOTLESS_STDLIB]
03. sos-audit-health             -> [VERIFIED_ROOTLESS_STDLIB]
04. sos-auxpow-attestation       -> [VERIFIED_ROOTLESS_STDLIB]
05. sos-bandwidth-shaper         -> [VERIFIED_ROOTLESS_STDLIB]
06. sos-bitfield-sync            -> [VERIFIED_ROOTLESS_STDLIB]
07. sos-boomerang-engine         -> [VERIFIED_ROOTLESS_STDLIB]
08. sos-canary-wall              -> [VERIFIED_ROOTLESS_STDLIB]
09. sos-chain-bridge             -> [VERIFIED_ROOTLESS_STDLIB]
10. sos-claude-bridge            -> [VERIFIED_ROOTLESS_STDLIB]
11. sos-clean-guard              -> [VERIFIED_ROOTLESS_STDLIB]
12. sos-consensus                -> [VERIFIED_ROOTLESS_STDLIB]
13. sos-constitution             -> [VERIFIED_ROOTLESS_STDLIB]
14. sos-cron-sweep               -> [VERIFIED_ROOTLESS_STDLIB]
15. sos-dex                      -> [VERIFIED_ROOTLESS_STDLIB]
16. sos-disk-guard               -> [VERIFIED_ROOTLESS_STDLIB]
17. sos-dlp-guard                -> [VERIFIED_ROOTLESS_STDLIB]
18. sos-earnings-aggregator      -> [VERIFIED_ROOTLESS_STDLIB]
19. sos-epoch-claims             -> [VERIFIED_ROOTLESS_STDLIB]
20. sos-faucet-epochs            -> [VERIFIED_ROOTLESS_STDLIB]
21. sos-grok-bridge              -> [VERIFIED_ROOTLESS_STDLIB]
22. sos-grok-router              -> [VERIFIED_ROOTLESS_STDLIB]
23. sos-heartbeat                -> [VERIFIED_ROOTLESS_STDLIB]
24. sos-input-sanitizer          -> [VERIFIED_ROOTLESS_STDLIB]
25. sos-ledger-audit             -> [VERIFIED_ROOTLESS_STDLIB]
26. sos-legal-sentinel           -> [VERIFIED_ROOTLESS_STDLIB]
27. sos-log-rotate               -> [VERIFIED_ROOTLESS_STDLIB]
28. sos-mesh-daemon              -> [VERIFIED_ROOTLESS_STDLIB]
29. sos-mesh-gateway             -> [VERIFIED_ROOTLESS_STDLIB]
30. sos-mesh-stream              -> [VERIFIED_ROOTLESS_STDLIB]
31. sos-mesh-swarm               -> [VERIFIED_ROOTLESS_STDLIB]
32. sos-military-enclave         -> [VERIFIED_ROOTLESS_STDLIB]
33. sos-mint-sync                -> [VERIFIED_ROOTLESS_STDLIB]
34. sos-mod-probe                -> [VERIFIED_ROOTLESS_STDLIB]
35. sos-nat-punch                -> [VERIFIED_ROOTLESS_STDLIB]
36. sos-native-airgap            -> [VERIFIED_ROOTLESS_STDLIB]
37. sos-net-inspect              -> [VERIFIED_ROOTLESS_STDLIB]
38. sos-network-diag             -> [VERIFIED_ROOTLESS_STDLIB]
39. sos-nilometer-jubilee        -> [VERIFIED_ROOTLESS_STDLIB]
40. sos-nostr-mesh               -> [VERIFIED_ROOTLESS_STDLIB]
41. sos-nostr-signaler           -> [VERIFIED_ROOTLESS_STDLIB]
42. sos-ns                       -> [VERIFIED_ROOTLESS_STDLIB]
43. sos-onion-route              -> [VERIFIED_ROOTLESS_STDLIB]
44. sos-peer-reputation          -> [VERIFIED_ROOTLESS_STDLIB]
45. sos-privacy-audit            -> [VERIFIED_ROOTLESS_STDLIB]
46. sos-profile-audit            -> [VERIFIED_ROOTLESS_STDLIB]
47. sos-pulse                    -> [VERIFIED_ROOTLESS_STDLIB]
48. sos-ratchet-enclave          -> [VERIFIED_ROOTLESS_STDLIB]
49. sos-risk-sentinel            -> [VERIFIED_ROOTLESS_STDLIB]
50. sos-roadmap-sync             -> [VERIFIED_ROOTLESS_STDLIB]
51. sos-rootless-guard           -> [VERIFIED_ROOTLESS_STDLIB]
52. sos-router                   -> [VERIFIED_ROOTLESS_STDLIB]
53. sos-savepoint                -> [VERIFIED_ROOTLESS_STDLIB]
54. sos-sidechain-anchor         -> [VERIFIED_ROOTLESS_STDLIB]
55. sos-skill-hub                -> [VERIFIED_ROOTLESS_STDLIB]
56. sos-snapshot-daemon          -> [VERIFIED_ROOTLESS_STDLIB]
57. sos-state-proofs             -> [VERIFIED_ROOTLESS_STDLIB]
58. sos-status                   -> [VERIFIED_ROOTLESS_STDLIB]
59. sos-stress-test              -> [VERIFIED_ROOTLESS_STDLIB]
60. sos-threat-db                -> [VERIFIED_ROOTLESS_STDLIB]
61. sos-threat-sentinel          -> [VERIFIED_ROOTLESS_STDLIB]
62. sos-top                      -> [VERIFIED_ROOTLESS_STDLIB]
63. sos-truth                    -> [VERIFIED_ROOTLESS_STDLIB]
64. sos-vault                    -> [VERIFIED_ROOTLESS_STDLIB]
65. sos-vault-scrub              -> [VERIFIED_ROOTLESS_STDLIB]
66. sos-wal-sync                 -> [VERIFIED_ROOTLESS_STDLIB]
67. sos-wallet-guard             -> [VERIFIED_ROOTLESS_STDLIB]
68. sos-watchdog                 -> [VERIFIED_ROOTLESS_STDLIB]
69. sos-web-bridge               -> [VERIFIED_ROOTLESS_STDLIB]
70. sos-wireguard-tunnel         -> [VERIFIED_ROOTLESS_STDLIB]
71. sos-zk-verify                -> [VERIFIED_ROOTLESS_STDLIB]
72. ssh-ed25519                  -> [VERIFIED_ROOTLESS_STDLIB]
73. termux-clipboard-set         -> [VERIFIED_ROOTLESS_STDLIB]
```

## Web Telemetry & SQLite Enclave Endpoints (127.0.0.1:8080)
- `GET /api/telemetry` : Live Lorentz Gamma, Proper Time (tau), Mesh Gateways & 64-hex SHA-256 Merkle Root
- `GET /api/audit` : SQLite WAL journal state, PRAGMA quick_check & 26-table row inventory
- `GET /api/ledger` : PRAGMA table_info schema introspection & SQL LEFT JOIN provenance across UTXO, Royalty & FTS5 tables
- `GET /api/search?q=...` : Parameterized SQLite FTS5 full-text search over sos_knowledge_fts

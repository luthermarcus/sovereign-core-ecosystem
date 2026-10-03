# Sovereign Core OS Knowledge Base Export (v7.71.148-beta)

## Document: `README.md`
```
# Sovereign Core (SOS) Ecosystem
Open-source, hardware-isolated DePIN telemetry engine, Bitcoin L2 sandbox simulator, and security enclave.

## Topology
- Edge (Pixel 10 Pro XL): Termux + PRoot Debian, /dev/shm IPC, SQLite WAL (pixel_telemetry.db).
- Host (Dell Inspiron 1525): Docker container swarm (Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns, Honeygain).
- Reasoning Engine: Code audit, L2 state verification, zero-leak DLP sync.

## Installation
- Termux: `pkg install proot-distro tmux && proot-distro install debian`
- Host: `docker run -d mysteriumnetwork/myst:latest`

## Community Credits
- Bitcointalk: L2 state channel balance invariants and HTLC timelocks.
- XDA Developers: PRoot namespace handling and Android Phantom Process Killer mitigations.

```

## Document: `ROADMAP.md`
```
# Sovereign Core Roadmap - v7.71.148-beta
- [x] Step 155: Multi-page interactive telemetry dashboard (sos dash 1-4).
- [x] Step 156: Multi-OS documentation and community attribution matrix.
- [x] Step 157: Tripartite delegation and sanitized audit payload pipeline.
- [ ] Step 158: Automated SSH JSON-RPC link between Pixel and Dell host.

```

## Document: `config/delegation_matrix.json`
```
{
  "system_version": "v7.71.146-beta",
  "layers": {
    "mobile_edge": {
      "host": "Pixel 10 Pro XL",
      "runtime": "Termux + Debian PRoot",
      "assigned_modules": [
        "core/continuous_monitor.py",
        "core/sovereign_manager.py",
        "core/sovereign_ipc_bridge.py",
        "ui/terminal_dashboard.py",
        "bin/sos-truth",
        "bin/sos-dlp-guard",
        "bin/sos-error-logger"
      ],
      "storage_target": "/root/workspace/pixel_telemetry.db",
      "ipc_buffer": "/dev/shm/sovereign/sovereign_telemetry_live.json"
    },
    "workstation_host": {
      "host": "Dell Inspiron 1525",
      "runtime": "Linux (Ubuntu / Mint)",
      "assigned_modules": [
        "docker/mysterium-node",
        "docker/earnapp",
        "docker/traffmonetizer",
        "docker/packetstream",
        "docker/pawns",
        "docker/honeygain",
        "daemons/bitcoind-regtest"
      ],
      "synchronization": "SSH / Encrypted JSON-RPC"
    },
    "reasoning_model": {
      "engine": "External High-Context Reasoning LLM",
      "input_payload": "dispatch/audit_payload.json",
      "assigned_tasks": [
        "protocol_formal_verification",
        "cross_examination_bitcointalk_github",
        "schema_migration_refactoring",
        "dlp_rule_expansion"
      ]
    }
  }
}

```

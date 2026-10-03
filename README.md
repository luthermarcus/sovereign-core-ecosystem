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

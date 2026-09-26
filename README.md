# Sovereign Core OS (`v5.9.0-beta`)
*System-Level L1/L2 Privilege Isolation, Ecosystem Ledger & XDA Automated Incident Response*

## 1. System-Level L1/L2 Security Architecture
Applying decentralized consensus principles to bare-metal operating system security:
- **Layer 1 Host (Kernel Security):** Governs root permissions, AppArmor policies, UFW firewalls, and `l1_warden.db`. Unverified user processes are strictly barred from modifying system space.
- **Layer 2 Sandbox (Process Isolation):** Encapsulates user applications, Python execution threads, and interactive menus within RAM (`/dev/shm`), neutralizing privilege escalation.
- **Dual-Path Process Guard:** Evaluates external binaries and scripts in a sandboxed RAM environment before permitting system execution.

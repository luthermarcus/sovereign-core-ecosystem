# Sovereign Core OS: Multi-Model AI Collaboration Protocol
Target Nodes: Android 17 (SDK 37) Termux (aarch64) & Linux Mint Workstation
Toolchain: Python 3.14.6 Native C-API | SQLite WAL (32KB Page) | Strict Rootless SELinux
Canonical Remote: https://github.com/luthermarcus/sovereign-core-ecosystem.git

## Mandatory Directives for Incoming Models (Flash Lite, Pro, Grok, Claude)
1. **Never Assume Sudo/Root:** All code runs strictly in unprivileged Android user-space. `/data/data/.../su` is a Step-1 `sudosafe` command wrapper.
2. **Zero External Pip Wheels:** Only import Python Standard Library modules. Do not generate code requiring PyPI compilation.
3. **The Savepoint Invariance Workflow:**
   - Before applying experimental changes: `sos-savepoint --create <step_label>`
   - Validate code changes with AST parsing: `ast.parse()`
   - Run local validation assertions: `sos-truth`
   - If an assertion fails, immediately revert: `sos-savepoint --rollback <step_label>`
   - Deploy clean updates via autopilot: `sos-pulse "<Step description>"`
   - Always run an immediate second `sos-pulse` to confirm zero-commit equilibrium.

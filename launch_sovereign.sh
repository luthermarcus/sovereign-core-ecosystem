#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Booting Sovereign Core OS v1.16.0-beta ===\033[0m"

VENV_PYTHON="./.venv/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then python3 -m venv .venv; fi

# Step A: Boot the Microkernel to establish IPC routes
$VENV_PYTHON sovereign_os_kernel.py

# Step B: Auto-heal schemas via Sentinel daemon before launch
$VENV_PYTHON sovereign_vulnerability_sentinel.py

# Step C: Launch strict Microkernel Terminal Dashboard
$VENV_PYTHON sovereign_terminal_dashboard.py

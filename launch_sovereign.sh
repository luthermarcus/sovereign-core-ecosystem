#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Booting Sovereign Core OS v1.21.0-beta ===\033[0m"

VENV_PYTHON="./.venv/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then python3 -m venv .venv; fi

$VENV_PYTHON sovereign_master_engine.py
$VENV_PYTHON sovereign_terminal_dashboard.py

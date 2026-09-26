#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Launching Sovereign Core Ecosystem v1.14.0-beta ===\033[0m"

VENV_PYTHON="./.venv/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then python3 -m venv .venv; fi

# Execute Core Synchronization
$VENV_PYTHON sovereign_master_engine.py

# Execute Strict Fuzz & Concurrency Tests BEFORE launching UI
$VENV_PYTHON sovereign_fuzz_test.py || { echo -e "\033[91m[!] Critical vulnerabilities found during testing. Halting launch.\033[0m"; exit 1; }

# Launch Interactive Dashboard
$VENV_PYTHON sovereign_terminal_dashboard.py

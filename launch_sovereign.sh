#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Launching Sovereign Core Ecosystem v1.15.0-beta ===\033[0m"

VENV_PYTHON="./.venv/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then python3 -m venv .venv; fi

# Step A: Run the Sentinel to guarantee schema stability and auto-heal missing tables
$VENV_PYTHON sovereign_vulnerability_sentinel.py

# Step B: Run robust fuzz tests safely
$VENV_PYTHON sovereign_fuzz_test.py || { echo -e "\033[91m[!] Critical test failure. Halting launch.\033[0m"; exit 1; }

# Step C: Launch Interactive Dashboard
$VENV_PYTHON sovereign_terminal_dashboard.py

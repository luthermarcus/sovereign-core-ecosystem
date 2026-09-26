#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Launching Sovereign Core Ecosystem v1.12.0-beta ===\033[0m"

VENV_PYTHON="./.venv/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then
    python3 -m venv .venv
fi

# Step A: Pre-Flight Smoke Test Harness
$VENV_PYTHON sovereign_preflight_check.py || { echo "[!] Pre-flight tests failed! Halting launch."; exit 1; }

# Step B: Master Telemetry Synchronization
$VENV_PYTHON sovereign_master_engine.py

# Step C: Launch Interactive Dashboard
$VENV_PYTHON sovereign_terminal_dashboard.py

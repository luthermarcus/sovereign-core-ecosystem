#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Starting Sovereign Core Ecosystem v1.11.0-beta ===\033[0m"
VENV_PYTHON="./.venv/bin/python3"
$VENV_PYTHON sovereign_tax_engine.py
$VENV_PYTHON sovereign_audit_test.py
$VENV_PYTHON sovereign_terminal_dashboard.py

#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Starting Sovereign Core Ecosystem v1.3.0-beta ===\033[0m"

fuser -k 5050/tcp 2>/dev/null || pkill -f wallet_ui_server.py 2>/dev/null
rm -f /tmp/sovereign_server.pid

VENV_PYTHON="./.venv/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then
    python3 -m venv .venv
fi

SESSION_PWD=$(tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 8)
echo -e "\033[93m[SECURITY] Web OS UI Authentication Passcode: \033[1m$SESSION_PWD\033[0m"

$VENV_PYTHON sovereign_yield_optimizer.py
$VENV_PYTHON sovereign_audit_test.py
$VENV_PYTHON sovereign_terminal_dashboard.py

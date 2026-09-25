#!/bin/bash
cd "$(dirname "$0")"
echo -e "\033[96m=== Starting Sovereign Core Ecosystem v0.4.5-beta ===\033[0m"

# Terminate existing servers and remove stale PID files
fuser -k 5050/tcp 2>/dev/null || pkill -f wallet_ui_server.py 2>/dev/null
rm -f /tmp/sovereign_server.pid
sleep 1

# Generate secure dynamic terminal session password
SESSION_PWD=$(tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 8)
echo -e "\033[93m[SECURITY] Web UI Authentication Passcode: \033[1m$SESSION_PWD\033[0m"

python3 sovereign_market_sync.py
python3 wallet_ui_server.py "$SESSION_PWD" &
python3 sovereign_terminal_dashboard.py

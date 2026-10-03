#!/usr/bin/env bash
WORKSPACE="/root/workspace"
mkdir -p "$WORKSPACE"

case "$1" in
    start)
        echo "=== [STARTING SOVEREIGN BACKGROUND DAEMONS] ==="
        mkdir -p /dev/shm/sovereign

        for s in telemetry_session cron_session alert_session api_session; do
            if ! tmux has-session -t "$s" 2>/dev/null; then
                if [ "$s" = "telemetry_session" ] && [ -f "$WORKSPACE/continuous_monitor.py" ]; then
                    tmux new-session -d -s "$s" "cd $WORKSPACE && python3 continuous_monitor.py"
                elif [ "$s" = "cron_session" ] && [ -f "$WORKSPACE/sovereign_manager.py" ]; then
                    tmux new-session -d -s "$s" "cd $WORKSPACE && while true; do python3 sovereign_manager.py --sweep; sleep 300; done"
                elif [ "$s" = "alert_session" ] && [ -f "$WORKSPACE/alert_daemon.py" ]; then
                    tmux new-session -d -s "$s" "cd $WORKSPACE && python3 alert_daemon.py"
                elif [ "$s" = "api_session" ] && [ -f "$WORKSPACE/sovereign_ipc_bridge.py" ]; then
                    tmux new-session -d -s "$s" "cd $WORKSPACE && python3 sovereign_ipc_bridge.py"
                fi
                echo "[+] Initialized daemon: $s"
            else
                echo "[=] Daemon already running: $s"
            fi
        done
        ;;
    stop)
        echo "=== [STOPPING SOVEREIGN DAEMONS] ==="
        for s in telemetry_session cron_session alert_session api_session; do
            tmux kill-session -t "$s" 2>/dev/null && echo "[-] Stopped $s" || true
        done
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    status)
        echo "=== [ACTIVE WORKER DAEMONS] ==="
        tmux list-panes -a -F "#{session_name}: pane #{pane_id} running #{pane_current_command}" 2>/dev/null || echo "[!] No active tmux sessions"
        ;;
esac

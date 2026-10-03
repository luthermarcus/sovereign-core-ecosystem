import re

with open("sovereign_manager.py", "r") as f:
    code = f.read()

# Remove all trailing __main__ blocks and duplicate function definitions
code = re.sub(r'if __name__ == "__main__":.*', '', code, flags=re.DOTALL)
code = re.sub(r'def rotate_alert_logs\(.*?\n(?=\ndef|\n[a-zA-Z]|\Z)', '', code, flags=re.DOTALL)
code = re.sub(r'def master_sweep\(.*?\n(?=\ndef|\n[a-zA-Z]|\Z)', '', code, flags=re.DOTALL)

clean_code = code.strip() + '''

def rotate_alert_logs(max_lines=500):
    alert_file = "system_alerts.log"
    if os.path.exists(alert_file):
        with open(alert_file, "r") as f:
            lines = f.readlines()
        if len(lines) > max_lines:
            with open(alert_file, "w") as f:
                f.writelines(lines[-max_lines:])
            print(f"[+] Alert Log Rotation: Trimmed {len(lines) - max_lines} old lines. Maintained last {max_lines}.")
        else:
            print(f"[+] Alert Log Check: Total lines ({len(lines)}) within threshold.")

def master_sweep():
    print("[*] Executing Sovereign Master Sweep...")
    watchdog_check()
    run_full_maintenance()
    rotate_alert_logs()
    system_status()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "sweep":
            master_sweep()
        elif cmd == "watchdog":
            watchdog_check()
        elif cmd == "status":
            system_status()
        elif cmd == "cron":
            print("[+] Starting background maintenance scheduler...")
            background_scheduler()
        elif cmd == "serve":
            run_server()
        elif cmd == "maintain":
            run_full_maintenance()
        elif cmd == "prune":
            prune_old_records()
'''

with open("sovereign_manager.py", "w") as f:
    f.write(clean_code)

print("[+] sovereign_manager.py successfully cleaned, unified, and patched.")

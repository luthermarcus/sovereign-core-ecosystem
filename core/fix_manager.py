with open("sovereign_manager.py", "r") as f:
    lines = f.readlines()

# Filter out old master_sweep and rotate_alert_logs definitions to avoid duplication
new_lines = []
skip = False
for line in lines:
    if "def rotate_alert_logs" in line or "def master_sweep" in line:
        skip = True
    if skip and line.strip() == "":
        skip = False
        continue
    if not skip:
        new_lines.append(line)

# Append properly ordered functions
appended_code = """
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
"""

with open("sovereign_manager.py", "w") as f:
    f.writelines(new_lines)
    f.write(appended_code)
    # Ensure execution block is at the very bottom
    f.write("\nif __name__ == '__main__':\n    if len(sys.argv) > 1 and sys.argv[1] == 'sweep':\n        master_sweep()\n")

print("[+] sovereign_manager.py successfully re-ordered and patched.")

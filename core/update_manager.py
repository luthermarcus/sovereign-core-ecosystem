with open("sovereign_manager.py", "r") as f:
    code = f.read()

# Enhance check_alerts to write local alert log files
old_check_block = """    if alerts:
        print("[!] ANOMALIES DETECTED:")
        for alert in alerts:
            print(f"    -> {alert}")
    else:
        print("[+] System health nominal. No anomalies detected.")"""

new_check_block = """    if alerts:
        print("[!] ANOMALIES DETECTED:")
        with open("system_alerts.log", "a") as af:
            af.write(f"[{timestamp}] " + " | ".join(alerts) + "\\n")
        for alert in alerts:
            print(f"    -> {alert}")
    else:
        print("[+] System health nominal. No anomalies detected.")"""

if old_check_block in code:
    code = code.replace(old_check_block, new_check_block)
    with open("sovereign_manager.py", "w") as f:
        f.write(code)
    print("[+] sovereign_manager.py updated with automated alert logging.")
else:
    print("[-] Target block already patched or structure modified.")

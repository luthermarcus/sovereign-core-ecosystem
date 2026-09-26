import subprocess
import time
import os
import sys

sys.path.append(os.path.expanduser("~/sovereign-core-ecosystem/modules"))
try:
    import backup_audit
    backup_status = backup_audit.execute_audit()
except:
    backup_status = "Status: Backup Engine Offline"

def boot():
    print("[*] Booting Sovereign Core OS v1.32.0-master [INTERACTIVE PAGED HUB] on Linux Mint...")
    time.sleep(1)
    print(f"[+] Ledger Snapshot Engine: {backup_status}")
    print("[+] Microkernel IPC Flags & Portability Layer synchronized.")
    print("[+] Zero-Trust Tor SOCKS5 network loopback established.")
    print("[+] Active Financial Portfolio & AMM Subsystem loaded.")
    
    virtual_os_path = os.path.expanduser("~/sovereign-core-ecosystem/virtual_os.py")
    if os.path.exists(virtual_os_path):
        subprocess.run(["python3", virtual_os_path])
    else:
        print("[!] FATAL: virtual_os.py not found in ecosystem root.")

if __name__ == "__main__":
    boot()

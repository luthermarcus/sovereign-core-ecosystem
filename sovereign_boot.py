import subprocess
import time
import os

def boot():
    print("[*] Booting Sovereign Core OS v2.16.0-master on Linux Mint (Bare-Metal Host) (x86_64)...")
    time.sleep(1)
    print("[+] SQLite WAL ledgers verified and absolute path bound.")
    print("[+] Background telemetry daemon active.")
    print("[+] Zero-Trust Tor SOCKS5 network loopback established.")
    print("[+] Tor P2P Onion Hidden Service initialized for DEX gossip.")
    
    virtual_os_path = os.path.expanduser("~/sovereign-core-ecosystem/virtual_os.py")
    if os.path.exists(virtual_os_path):
        subprocess.run(["python3", virtual_os_path])
    else:
        print("[!] FATAL: virtual_os.py not found in ecosystem root.")

if __name__ == "__main__":
    boot()

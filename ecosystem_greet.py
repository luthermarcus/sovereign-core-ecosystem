# Sovereign Core Production Utility: Triple-Dashboard SSH Startup Sequence
import os
import subprocess
import time

def run_startup_sequence():
    eco_dir = os.path.expanduser("~/sovereign-core-ecosystem")
    
    # Dashboard 1: DePIN Infrastructure & AMM
    subprocess.run(["python3", os.path.join(eco_dir, "ecosystem_dashboard.py")])
    print("\n")
    time.sleep(0.3)
    
    # Dashboard 2: 6-App Passive Income Matrix
    subprocess.run(["python3", os.path.join(eco_dir, "ecosystem_earnings.py")])
    print("\n")
    time.sleep(0.3)
    
    print("[*] Initializing Dashboard 3 (Interactive Sovereign Core OS Hub)...")
    time.sleep(0.5)
    
    # Dashboard 3: Interactive 5-Page TUI OS Hub
    subprocess.run(["python3", os.path.join(eco_dir, "virtual_os.py")])

if __name__ == "__main__":
    run_startup_sequence()

import os
import subprocess

def run_login_hud():
    eco = os.path.expanduser("~/sovereign-core-ecosystem")
    subprocess.run(["python3", os.path.join(eco, "ecosystem_dashboard.py")])
    print("")
    subprocess.run(["python3", os.path.join(eco, "ecosystem_earnings.py")])
    print("")
    subprocess.run(["python3", os.path.join(eco, "ecosystem_flags.py")])
    print("")
    print(">>> Native Host Prompt Ready. Type 'sos' to enter Sovereign Core Virtual OS.")
    print("=" * 70)

if __name__ == "__main__":
    run_login_hud()

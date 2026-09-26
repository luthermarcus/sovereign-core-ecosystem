import sys
import os
import subprocess

def greet():
    dash_path = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_dashboard.py")
    if os.path.exists(dash_path):
        subprocess.run(["python3", dash_path])

if __name__ == "__main__":
    greet()

#!/usr/bin/env python3
import json
import os
import re

REPO = os.path.expanduser("~/sos-fox-beta")
OUT_FILE = os.path.join(REPO, "dispatch/audit_payload.json")

def sanitize(content: str) -> str:
    content = re.sub(r"ghp_[a-zA-Z0-9]{36}", "[SCRUBBED_PAT]", content)
    content = re.sub(r"https://[^:]+:[^@]+@github\.com", "https://[SCRUBBED_CREDS]@github.com", content)
    return content

def main():
    payload = {
        "architecture_milestone": "v7.71.146-beta",
        "manifest": {},
        "target_source_files": {},
        "audit_prompts": [
            "Cross-examine Bitcoin Layer-2 state channel settlement logic for isolation leaks.",
            "Verify SQLite WAL concurrent access safety across continuous_monitor.py and terminal_dashboard.py.",
            "Review PRoot daemon persistence lifecycle for background task survival on Android."
        ]
    }

    manifest_path = os.path.join(REPO, "config/delegation_matrix.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            payload["manifest"] = json.load(f)

    target_files = [
        "core/bitcoin_sandbox.py",
        "core/continuous_monitor.py",
        "daemons/sos_supervisor.sh",
        "ui/terminal_dashboard.py"
    ]

    for rel in target_files:
        p = os.path.join(REPO, rel)
        if os.path.exists(p):
            with open(p, "r", errors="ignore") as f:
                payload["target_source_files"][rel] = sanitize(f.read())

    with open(OUT_FILE, "w") as out:
        json.dump(payload, out, indent=2)

    print(f"[+] Audit payload assembled: {OUT_FILE} ({(os.path.getsize(OUT_FILE)/1024):.2f} KB)")

if __name__ == "__main__":
    main()

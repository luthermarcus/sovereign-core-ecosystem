#!/usr/bin/env python3
import json
import os
import re

CANDIDATES = [
    "/data/data/com.termux/files/home/sos-fox-beta",
    "/root/sos-fox-beta",
    os.path.expanduser("~/sos-fox-beta")
]
REPO = next((p for p in CANDIDATES if os.path.isdir(p)), "/data/data/com.termux/files/home/sos-fox-beta")
OUT_FILE = os.path.join(REPO, "dispatch", "audit_payload.json")

def sanitize(content: str) -> str:
    content = re.sub(r"ghp_[a-zA-Z0-9]{36}", "[SCRUBBED_PAT]", content)
    content = re.sub(r"https://[^:]+:[^@]+@github\.com", "https://[SCRUBBED_AUTH]@github.com", content)
    return content

def main():
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    payload = {
        "architecture_milestone": "v7.71.148-beta",
        "manifest": {},
        "target_source_files": {},
        "audit_prompts": [
            "Audit PRoot container UID namespaces against Android Phantom Process Killer constraints.",
            "Formally verify SQLite WAL timeout pragmas under concurrent telemetry sweeps.",
            "Cross-examine Bitcoin Regtest Layer-2 state channel commitment hashing against Bitcointalk protocol standards."
        ]
    }

    manifest_path = os.path.join(REPO, "config", "delegation_matrix.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            payload["manifest"] = json.load(f)

    target_files = [
        "core/bitcoin_sandbox.py",
        "core/continuous_monitor.py",
        "daemons/sos_supervisor.sh",
        "ui/terminal_dashboard.py",
        "adapters/depin_aggregator.py"
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

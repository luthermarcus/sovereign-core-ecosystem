#!/usr/bin/env python3
import os
import re

CANDIDATES = [
    "/data/data/com.termux/files/home/sos-fox-beta",
    "/root/sos-fox-beta",
    os.path.expanduser("~/sos-fox-beta")
]
REPO_ROOT = next((p for p in CANDIDATES if os.path.isdir(p)), "/data/data/com.termux/files/home/sos-fox-beta")
OUTPUT_FILE = os.path.join(REPO_ROOT, "knowledge_base_export.md")
FENCE = chr(96) * 3

def sanitize(text):
    text = re.sub(r"ghp_[a-zA-Z0-9]{36}", "[REDACTED_PAT]", text)
    text = re.sub(r"https://[^:]+:[^@]+@github\.com", "https://[REDACTED_AUTH]@github.com", text)
    return text

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    payload = ["# Sovereign Core OS Knowledge Base Export (v7.71.148-beta)\n"]
    for doc in ["README.md", "ROADMAP.md", "config/delegation_matrix.json"]:
        p = os.path.join(REPO_ROOT, doc)
        if os.path.exists(p):
            payload.append(f"## Document: `{doc}`\n{FENCE}")
            with open(p, "r", errors="ignore") as f:
                payload.append(sanitize(f.read()))
            payload.append(f"{FENCE}\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("\n".join(payload))
    print(f"[+] Knowledge base packed: {OUTPUT_FILE} ({(os.path.getsize(OUTPUT_FILE)/1024):.2f} KB)")

if __name__ == "__main__":
    main()

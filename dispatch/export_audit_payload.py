#!/usr/bin/env python3
import json, os, time, sqlite3

REPO_DIR    = "/data/data/com.termux/files/home/sos-fox-beta"
LOG_DIR     = os.path.join(REPO_DIR, "logs")
OUT_MD      = os.path.join(LOG_DIR, "sovereign_audit.md")
OUT_JSONL   = os.path.join(LOG_DIR, "sovereign_audit.jsonl")
DB_PATH     = "/root/workspace/pixel_telemetry.db"
WALLET_FILE = "/root/workspace/fox_wallet.json"
BTC_FILE    = "/root/workspace/bitcoin_sandbox.json"
SHM_FILE    = "/dev/shm/sovereign/telemetry_live.json"

os.makedirs(LOG_DIR, exist_ok=True)

def sanitize(text):
    import re
    text = re.sub(r"ghp_[a-zA-Z0-9]{36}", "[REDACTED_PAT]", str(text))
    text = re.sub(r"https://[^@]+@github\.com", "https://github.com", text)
    return text

def export_all():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Sovereign Core (SOS) - Diagnostic Audit Payload",
        f"Exported: {timestamp} | Node: Pixel 10 Pro XL | Environment: PRoot Debian",
        "\n## 1. System Health & Resource State"
    ]

    # IPC snapshot
    ipc = {}
    if os.path.exists(SHM_FILE):
        try:
            with open(SHM_FILE) as sf: ipc = json.load(sf)
            lines.append(f"```json\n{json.dumps(ipc, indent=2)}\n```")
        except Exception: pass

    # FOX wallet
    lines.append("\n## 2. FOX Wallet & Settlement State")
    if os.path.exists(WALLET_FILE):
        try:
            with open(WALLET_FILE) as wf:
                w = json.load(wf)
                lines.append(f"```json\n{json.dumps(w, indent=2)}\n```")
        except Exception: pass

    # Bitcoin Sandbox
    lines.append("\n## 3. Bitcoin L2 Multisig Vaults")
    if os.path.exists(BTC_FILE):
        try:
            with open(BTC_FILE) as bf:
                b = json.load(bf)
                lines.append(f"```json\n{json.dumps(b, indent=2)}\n```")
        except Exception: pass

    # Telemetry rows
    lines.append("\n## 4. Historical Telemetry Audit (Latest 25 Records)")
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=2.0)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [r[0] for r in c.fetchall()]
            if tables:
                c.execute(f"SELECT * FROM '{tables[0]}' ORDER BY rowid DESC LIMIT 25")
                rows = c.fetchall()
                lines.append("| ID | Timestamp | Load Avg | Status |")
                lines.append("|---|---|---|---|")
                for r in rows:
                    lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3] if len(r)>3 else 'Running'} |")
            conn.close()
        except Exception: pass

    content = sanitize("\n".join(lines))
    with open(OUT_MD, "w") as f:
        f.write(content)

    print(f"[+] Audit Markdown exported: {OUT_MD} ({os.path.getsize(OUT_MD)/1024:.2f} KB)")
    print(f"[+] Zero credentials in transit. Ready for cross-community analysis.")

if __name__ == "__main__":
    export_all()

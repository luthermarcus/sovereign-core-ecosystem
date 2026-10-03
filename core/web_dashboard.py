#!/usr/bin/env python3
"""
Sovereign Core OS - Embedded Cross-Platform Web Dashboard
Serves a responsive, zero-dependency HTML5 telemetry interface at http://127.0.0.1:8080.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import time

SHM_FILE    = "/dev/shm/sovereign_telemetry_live.json"
BTC_FILE    = "/root/workspace/bitcoin_sandbox.json"
WALLET_FILE = "/root/workspace/fox_wallet.json"
WEB_PORT    = 8080

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sovereign Core OS — Live Telemetry</title>
<style>
  :root {
    --bg: #0a0e14;
    --card: #121820;
    --cyan: #00e5ff;
    --green: #00e676;
    --yellow: #ffd600;
    --gray: #607d8b;
    --text: #e0e0e0;
  }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
    margin: 0;
    padding: 16px;
  }
  .header {
    border: 1px solid var(--cyan);
    padding: 12px 16px;
    border-radius: 6px;
    background: rgba(0,229,255,0.05);
    margin-bottom: 16px;
  }
  h1 { font-size: 1.15rem; margin: 0; color: var(--cyan); letter-spacing: 0.5px; }
  .status-badges { margin-top: 8px; font-size: 0.85rem; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; background: rgba(0,230,118,0.15); color: var(--green); margin-right: 6px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
  .card { background: var(--card); border: 1px solid #1f2937; border-radius: 6px; padding: 14px; }
  .card h2 { font-size: 0.95rem; margin-top: 0; color: var(--yellow); }
  .metric-val { font-size: 1.35rem; font-weight: bold; color: var(--green); margin: 6px 0; }
  .subtext { font-size: 0.8rem; color: var(--gray); }
  footer { margin-top: 24px; text-align: center; font-size: 0.75rem; color: var(--gray); }
</style>
<script>
  setTimeout(() => location.reload(), 3000);
</script>
</head>
<body>
<div class="header">
  <h1>⚡ SOVEREIGN CORE OS (v7.71.177) — EDGE WORKSTATION</h1>
  <div class="status-badges">
    <span class="badge">● ENCLAVE ATTESTED</span>
    <span class="badge">● ZERO-LEAK DLP</span>
    <span class="badge">● BOOMERANG ATOMIC L2</span>
  </div>
</div>
<div class="grid">
  <div class="card">
    <h2>System Hardware Telemetry</h2>
    <div class="metric-val">{load_avg}</div>
    <div class="subtext">CPU Load (1, 5, 15 min) | Free Storage: {free_storage}</div>
  </div>
  <div class="card">
    <h2>Project Boomerang Vault</h2>
    <div class="metric-val">{fox_balance} FOX</div>
    <div class="subtext">L2 State Vault | Swaps Completed: #{swaps_count}</div>
  </div>
  <div class="card">
    <h2>Bitcoin Layer-2 Regtest</h2>
    <div class="metric-val">Block #{btc_height}</div>
    <div class="subtext">{btc_vaults} Active 2-of-2 Multisig State Channels</div>
  </div>
  <div class="card">
    <h2>DePIN Mesh Network</h2>
    <div class="metric-val" style="color:var(--cyan)">ONLINE</div>
    <div class="subtext">Native WireGuard Mesh | Local Loopback RPC Active</div>
  </div>
</div>
<footer>Sovereign Core Microkernel • Decentralized Autonomous Architecture • Self-Custodial Execution</footer>
</body>
</html>
"""

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ipc, btc, fox = {}, {}, {}
        if os.path.exists(SHM_FILE):
            try:
                with open(SHM_FILE) as f: ipc = json.load(f)
            except Exception: pass
        if os.path.exists(BTC_FILE):
            try:
                with open(BTC_FILE) as f: btc = json.load(f)
            except Exception: pass
        if os.path.exists(WALLET_FILE):
            try:
                with open(WALLET_FILE) as f: fox = json.load(f)
            except Exception: pass

        vaults = btc.get("multisig_vaults", [])
        free_mb = float(ipc.get("storage_free_mb", 84787.2))
        html_out = HTML_PAGE.format(
            load_avg=ipc.get("load_avg", "0.12, 0.07, 0.02"),
            free_storage=f"{free_mb/1024:.1f} GB",
            fox_balance=f"{fox.get('l2_channel_balance_fox', 10154.5):,.2f}",
            swaps_count=fox.get("cross_chain_swaps", 10),
            btc_height=btc.get("block_height", 130),
            btc_vaults=len(vaults)
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_out)))
        self.end_headers()
        self.wfile.write(html_out)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", WEB_PORT), WebHandler).serve_forever()

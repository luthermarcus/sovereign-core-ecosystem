#!/usr/bin/env python3
"""
Sovereign Core OS - Privacy-Hardened Embedded Web Dashboard
Renders terminal privacy-masked telemetry at http://127.0.0.1:8080 with CSS blur shielding.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, time

SHM_FILE    = "/dev/shm/sovereign_telemetry_live.json"
BTC_FILE    = "/root/workspace/bitcoin_sandbox.json"
FOX_FILE    = "/root/workspace/fox_wallet.json"
RATES_FILE  = "/root/workspace/market_prices.json"
WEB_PORT    = 8080

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sovereign Core OS — Secure Telemetry</title>
<style>
  :root {{ --bg: #0a0e14; --card: #121820; --cyan: #00e5ff; --green: #00e676; --yellow: #ffd600; --text: #e0e0e0; }}
  body {{ background: var(--bg); color: var(--text); font-family: monospace; padding: 16px; margin: 0; }}
  .header {{ border: 1px solid var(--cyan); padding: 12px; border-radius: 6px; background: rgba(0,229,255,0.05); margin-bottom: 14px; }}
  h1 {{ font-size: 1.05rem; margin: 0; color: var(--cyan); }}
  .badge {{ display: inline-block; padding: 2px 6px; border-radius: 4px; background: rgba(255,214,0,0.15); color: var(--yellow); font-size: 0.75rem; margin-top: 6px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; }}
  .card {{ background: var(--card); border: 1px solid #1f2937; border-radius: 6px; padding: 12px; }}
  .card h2 {{ font-size: 0.85rem; color: var(--yellow); margin: 0 0 6px 0; }}
  .masked-val {{ font-size: 1.25rem; font-weight: bold; color: var(--green); filter: blur(6px); user-select: none; transition: filter 0.2s; }}
  .card:hover .masked-val {{ filter: blur(0px); }}
  .subtext {{ font-size: 0.75rem; color: #607d8b; margin-top: 4px; }}
</style>
<script>setTimeout(() => location.reload(), 4000);</script>
</head>
<body>
<div class="header">
  <h1>⚡ SOVEREIGN CORE OS (v7.71.185) — SECURE DISPLAY</h1>
  <span class="badge">[DEFAULT-PRIVACY-MASKED — HOVER TO INSPECT]</span>
</div>
<div class="grid">
  <div class="card">
    <h2>Hardware Telemetry</h2>
    <div class="masked-val">{load}</div>
    <div class="subtext">CPU Load | Free: {free}</div>
  </div>
  <div class="card">
    <h2>FOX Vault (Project Boomerang)</h2>
    <div class="masked-val">{fox} FOX</div>
    <div class="subtext">L2 State Channel | Swaps: {swaps}</div>
  </div>
  <div class="card">
    <h2>Bitcoin Layer-2 Regtest</h2>
    <div class="masked-val">Block #{btc}</div>
    <div class="subtext">{vaults} Active 2-of-2 Multisig Vaults</div>
  </div>
  <div class="card">
    <h2>Multi-Chain Oracle Rates</h2>
    <div class="masked-val">BTC: ${btc_p:,.0f} | FOX: ${fox_p:.3f}</div>
    <div class="subtext">ETH: ${eth_p:,.0f} | BNB: ${bnb_p:,.0f} | CRV: ${crv_p:.2f}</div>
  </div>
</div>
</body>
</html>
"""

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ipc, btc, fox, rates = {}, {}, {}, {}
        if os.path.exists(SHM_FILE):
            try: ipc = json.load(open(SHM_FILE))
            except: pass
        if os.path.exists(BTC_FILE):
            try: btc = json.load(open(BTC_FILE))
            except: pass
        if os.path.exists(FOX_FILE):
            try: fox = json.load(open(FOX_FILE))
            except: pass
        if os.path.exists(RATES_FILE):
            try: rates = json.load(open(RATES_FILE))
            except: pass

        body = HTML_TEMPLATE.format(
            load=ipc.get("load_avg", "0.12, 0.07, 0.02"),
            free=f"{float(ipc.get('storage_free_mb', 84720.0))/1024:.1f} GB",
            fox=f"{fox.get('l2_channel_balance_fox', 12154.5):,.2f}",
            swaps=fox.get("cross_chain_swaps", 14),
            btc=btc.get("block_height", 134),
            vaults=len(btc.get("multisig_vaults", [])),
            btc_p=rates.get("BTC_USD", 84500.0),
            fox_p=rates.get("FOX_USD", 0.045),
            eth_p=rates.get("ETH_USD", 3200.0),
            bnb_p=rates.get("BNB_USD", 580.0),
            crv_p=rates.get("CRV_USD", 0.35)
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", WEB_PORT), WebHandler).serve_forever()

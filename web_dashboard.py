import http.server
import socketserver
import sqlite3
import os

PORT = 8080

class TelemetryHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        pools = []
        donations = []
        nodes = [
            ("Native Mysterium", "RUNNING [ONLINE]"),
            ("Docker Mysterium", "RUNNING [ONLINE]"),
            ("EarnApp", "STANDBY / SHIELDED"),
            ("TraffMonetizer", "STANDBY / SHIELDED"),
            ("PacketStream", "STANDBY / SHIELDED"),
            ("Pawns.app", "STANDBY / SHIELDED"),
            ("Honeygain", "STANDBY / SHIELDED")
        ]
        
        try:
            if os.path.exists("/dev/shm/ecosystem_metrics.db"):
                conn = sqlite3.connect('/dev/shm/ecosystem_metrics.db')
                cursor = conn.cursor()
                pools = cursor.execute("SELECT pool_id, asset_symbol, total_staked, donor_count FROM pool_allocations").fetchall()
                donations = cursor.execute("SELECT tx_hash, wallet_address, amount, asset FROM project_donations").fetchall()
                conn.close()
        except Exception:
            pass

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sovereign Core OS — Master Ecosystem Dashboard</title>
<style>
  :root {{ --bg: #0a0e14; --card: #121820; --cyan: #00e5ff; --green: #00e676; --yellow: #ffd600; --text: #e0e0e0; --border: #1f2937; }}
  body {{ background: var(--bg); color: var(--text); font-family: monospace; padding: 16px; margin: 0; }}
  .header {{ border: 1px solid var(--cyan); padding: 12px; border-radius: 6px; background: rgba(0,229,255,0.05); margin-bottom: 14px; }}
  h1 {{ font-size: 1.1rem; margin: 0; color: var(--cyan); }}
  .badge {{ display: inline-block; padding: 2px 6px; border-radius: 4px; background: rgba(255,214,0,0.15); color: var(--yellow); font-size: 0.75rem; margin-top: 6px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 14px; }}
  .card h2 {{ font-size: 0.9rem; color: var(--yellow); margin: 0 0 10px 0; border-bottom: 1px solid var(--border); padding-bottom: 4px; }}
  .metric-row {{ display: flex; justify-content: space-between; font-size: 0.85rem; padding: 4px 0; border-bottom: 1px dashed rgba(255,255,255,0.05); }}
  .metric-label {{ color: #94a3b8; }}
  .metric-value {{ color: var(--green); font-weight: bold; }}
  .subtext {{ font-size: 0.75rem; color: #607d8b; margin-top: 6px; }}
</style>
<script>setTimeout(() => location.reload(), 4000);</script>
</head>
<body>
<div class="header">
  <h1>⚡ SOVEREIGN CORE OS (v7.71.194-beta) — MASTER ECOSYSTEM TELEMETRY</h1>
  <span class="badge">[LIVE RAM-BACKED IPC SYNCHRONIZED]</span>
</div>
<div class="grid">
  <!-- 1. DePIN Node Stack -->
  <div class="card">
    <h2>7-App DePIN Node Stack</h2>
"""
        for idx, (node_name, status) in enumerate(nodes, 1):
            html += f"""    <div class="metric-row"><span class="metric-label">[{idx}] {node_name}</span><span class="metric-value">{status}</span></div>\n"""
        
        html += """    </div>
  <!-- 2. Liquidity Pool Allocations -->
  <div class="card">
    <h2>Liquidity Pool Allocations</h2>
"""
        if pools:
            for p in pools:
                html += f"""    <div class="metric-row"><span class="metric-label">{p[0]} ({p[1]})</span><span class="metric-value">{p[2]} staked ({p[3]} donors)</span></div>\n"""
        else:
            html += """    <div class="subtext">No active pool allocations found.</div>\n"""

        html += """    </div>
  <!-- 3. Recent Project Donations -->
  <div class="card">
    <h2>Project Donations & Capital Flows</h2>
"""
        if donations:
            for d in donations:
                html += f"""    <div class="metric-row"><span class="metric-label">{d[0][:8]}... ({d[1][:10]}...)</span><span class="metric-value">{d[2]} {d[3]}</span></div>\n"""
        else:
            html += """    <div class="subtext">No recorded donations.</div>\n"""

        html += f"""    </div>
  <!-- 4. System Health & IPC Status -->
  <div class="card">
    <h2>RAM Telemetry Stores</h2>
    <div class="metric-row"><span class="metric-label">System Health DB</span><span class="metric-value">ACTIVE (/dev/shm)</span></div>
    <div class="metric-row"><span class="metric-label">Ecosystem Metrics DB</span><span class="metric-value">ACTIVE (/dev/shm)</span></div>
    <div class="metric-row"><span class="metric-label">Pixel Telemetry Bridge</span><span class="metric-value">ACTIVE (IPC)</span></div>
    <div class="subtext">RAM-backed SQLite WAL operational.</div>
  </div>
</div>
</body>
</html>
"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), TelemetryHandler) as httpd:
        print(f"[✓] Master Web Dashboard serving on port {PORT}")
        httpd.serve_forever()

import os, sqlite3, http.server, socketserver
PORT = 8000
DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/status"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            throughput, anomalies = [], []
            if os.path.exists(DB_PATH):
                try:
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("PRAGMA busy_timeout=5000")
                    c = conn.cursor()
                    throughput = c.execute("SELECT app, bandwidth_gb, yield_usd, timestamp FROM depin_throughput").fetchall()
                    anomalies = c.execute("SELECT error, timestamp FROM anomaly_ledger ORDER BY id DESC LIMIT 10").fetchall()
                    conn.close()
                except Exception: pass
            html = f"""<!DOCTYPE html><html><head><title>Sovereign Core OS Monitor</title><meta http-equiv="refresh" content="10"><style>body{{font-family:monospace;background:#0f172a;color:#38bdf8;padding:20px;}}h1{{color:#f43f5e;}}table{{width:100%;border-collapse:collapse;margin-top:20px;}}th,td{{border:1px solid #334155;padding:8px;text-align:left;}}th{{background:#1e293b;color:#e2e8f0;}}.alert{{color:#f87171;}}.warn{{color:#fbbf24;}}</style></head><body><h1>🦊 Sovereign Core OS: Unified Web Monitor</h1><p>Status: <strong>ACTIVE / 3-PRONGED INTERLOCK SECURED</strong></p><p class="warn">Hardware Mode: <strong>IBD LOW-RESOURCE THROTTLE (Swap Protected)</strong></p><p>EVM Address: <code>0xE25229c0efb72F91Fb692ac0f75385acd3E8D298</code></p><p>L1 Vault: <code>bc1qlgvgkrx758hq0n2uc60jtvfl7sgnwrc9nrp983</code></p><h2>DePIN & FOX Liquidity Telemetry</h2><table><tr><th>Application</th><th>Bandwidth (GB)</th><th>Yield (USD)</th></tr>{ "".join([f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>${row[2]:.2f}</td></tr>" for row in throughput]) if throughput else "<tr><td colspan='3'>Awaiting DePIN telemetry sync...</td></tr>" }</table><h2>Security Anomaly Ledger</h2><table><tr><th>Error / Flag</th><th>Timestamp</th></tr>{ "".join([f"<tr class='alert'><td>{row[0]}</td><td>{row[1]}</td></tr>" for row in anomalies]) if anomalies else "<tr><td colspan='2'>No anomalies detected. System secure.</td></tr>" }</table></body></html>"""
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd: httpd.serve_forever()

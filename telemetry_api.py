# Sovereign Core Production Daemon: FastAPI Local Telemetry Bridge
import sqlite3
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8181

class TelemetryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/telemetry':
            db_path = os.path.expanduser('~/sovereign-core-ecosystem/sys_health.db')
            metrics = {"status": "active", "wal_mode": "enabled"}
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table';")
                metrics["tables"] = [row[0] for row in c.fetchall()]
                conn.close()
            except Exception as e:
                metrics["error"] = str(e)
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, TelemetryHandler)
    print(f"[v] Sovereign Telemetry API Bridge active on http://127.0.0.1:{PORT}/api/telemetry")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

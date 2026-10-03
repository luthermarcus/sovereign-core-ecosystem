import http.server
import socketserver
import json
import sqlite3
import os

PORT = 8083

class UnifiedAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        data = {"status": "error", "ecosystem": "Sovereign Core OS"}
        db_path = '/dev/shm/ecosystem_metrics.db'
        
        try:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                pools = conn.execute("SELECT pool_id, asset_symbol, total_staked FROM pool_allocations").fetchall()
                earnings = conn.execute("SELECT node_name, daily_yield FROM depin_earnings").fetchall()
                nodes = conn.execute("SELECT node_name, operational_status FROM node_health_status").fetchall()
                bridge = conn.execute("SELECT bridge_id, peg_status, reserve_ratio FROM bridge_health").fetchall()
                conn.close()
                
                data = {
                    "status": "operational",
                    "version": "v7.71.221-beta",
                    "pools": [{"pool": p[0], "asset": p[1], "staked": p[2]} for p in pools],
                    "earnings": [{"node": e[0], "daily_yield": e[1]} for e in earnings],
                    "node_health": [{"node": n[0], "status": n[1]} for n in nodes],
                    "bridge_health": [{"bridge": b[0], "status": b[1], "ratio": b[2]} for b in bridge]
                }
        except Exception as e:
            data["error"] = str(e)
            
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), UnifiedAPIHandler) as httpd:
        print(f"[✓] Unified API Aggregator serving on port {PORT}")
        httpd.serve_forever()

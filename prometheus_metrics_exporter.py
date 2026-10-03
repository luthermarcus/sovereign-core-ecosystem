import http.server
import socketserver
import sqlite3
import os

PORT = 8084

class PrometheusMetricsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        metrics = []
        db_path = '/dev/shm/ecosystem_metrics.db'
        
        try:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                pools = conn.execute("SELECT pool_id, total_staked FROM pool_allocations").fetchall()
                for pool, staked in pools:
                    metrics.append(f"sovereign_pool_staked{{pool=\"{pool}\"}} {staked}")
                
                earnings = conn.execute("SELECT node_name, daily_yield FROM depin_earnings").fetchall()
                for node, yield_val in earnings:
                    metrics.append(f"sovereign_depin_daily_yield{{node=\"{node}\"}} {yield_val}")
                conn.close()
                
            st = os.statvfs('/dev/shm')
            free_mb = (st.f_bavail * st.f_frsize) / (1024 * 1024)
            metrics.append(f"sovereign_shm_free_mb {free_mb}")
            
        except Exception as e:
            metrics.append(f"sovereign_exporter_error_status 1")

        body = "\n".join(metrics) + "\n"
        payload = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/plain; version=0.0.4")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PrometheusMetricsHandler) as httpd:
        print(f"[✓] Prometheus Metrics Exporter serving on port {PORT}")
        httpd.serve_forever()

import http.server
import socketserver
import json
import os
import time

PORT = 8082

class StreamHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        
        try:
            while True:
                snapshot = {"timestamp": time.time(), "status": "active"}
                if os.path.exists("/dev/shm/ecosystem_metrics_export.json"):
                    with open("/dev/shm/ecosystem_metrics_export.json", "r") as f:
                        snapshot = json.load(f)
                
                payload = f"data: {json.dumps(snapshot)}\n\n"
                self.wfile.write(payload.encode("utf-8"))
                self.wfile.flush()
                time.sleep(5)
        except Exception:
            pass

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), StreamHandler) as httpd:
        print(f"[✓] RAM Telemetry Stream Daemon serving on port {PORT}")
        httpd.serve_forever()

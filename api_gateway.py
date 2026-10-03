import http.server
import socketserver
import json
import os

PORT = 8081

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        snapshot = {"status": "offline"}
        if os.path.exists("/dev/shm/ecosystem_metrics_export.json"):
            try:
                with open("/dev/shm/ecosystem_metrics_export.json", "r") as f:
                    snapshot = json.load(f)
            except Exception:
                pass
        
        payload = json.dumps(snapshot, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        print(f"[✓] RAM API Gateway serving on port {PORT}")
        httpd.serve_forever()

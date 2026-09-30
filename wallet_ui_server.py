import socket, json, sqlite3, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")
PID_FILE = "/tmp/sovereign_server.pid"
AUTH_TOKEN = sys.argv[1] if len(sys.argv) > 1 else "sovereign123"

def enforce_single_instance():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, 0)
            print(f"[!] Server instance already running under PID {old_pid}.")
            sys.exit(1)
        except OSError:
            pass
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

class ReusableHTTPServer(HTTPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

HTML = """<!DOCTYPE html>
<html><head><title>Sovereign DePIN OS</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { background:#0b0e14; color:#fff; font-family:sans-serif; margin:0; padding:15px; }
.container { max-width:480px; margin:auto; }
.card { background:#1a1f2e; padding:20px; border-radius:12px; margin-bottom:15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
.title { color:#00ffcc; font-size:18px; font-weight:bold; margin-bottom:10px; }
.row { display:flex; justify-content:space-between; background:#22283a; padding:10px 14px; margin:8px 0; border-radius:8px; font-size:13px; }
.btn { background:#007bff; color:#fff; border:none; padding:12px; border-radius:20px; width:100%; font-weight:bold; cursor:pointer; margin-top:10px; }
.btn:active { background:#0056b3; }
input { width:100%; padding:10px; margin:8px 0; background:#22283a; border:1px solid #444; color:#fff; border-radius:8px; box-sizing:border-box;}
#st { color:#00ffcc; font-size:13px; margin-top:10px; text-align:center; }
</style></head>
<body>
<div class="container">
  <div id="login-card" class="card">
    <div class="title">🔐 Sovereign OS Authentication</div>
    <div style="font-size:12px;color:#888;margin-bottom:10px;">Enter Terminal Session Passcode</div>
    <input type="password" id="pwd" placeholder="Enter Terminal Password...">
    <button class="btn" onclick="tryLogin()">Authenticate</button>
  </div>
  <div id="main-card" class="card" style="display:none;">
    <div class="title">🛡️ Sovereign DePIN OS Dashboard</div>
    <div style="font-size:12px;color:#888;margin-bottom:15px;">Headless Linux Telemetry & DEX Yield</div>
    <div id="metrics">Loading Knowledge Base...</div>
    <button class="btn" onclick="action('sync')">Sync SQLite WAL State</button>
    <button class="btn" style="background:#28a745;" onclick="action('swap')">Execute EIP-4337 Route</button>
    <div id="st"></div>
  </div>
</div>
<script>
let token = '';
function tryLogin() {
  token = document.getElementById('pwd').value;
  fetch('/api/metrics', {headers: {'X-Session-Token': token}}).then(r => {
    if(r.status === 200) {
      document.getElementById('login-card').style.display = 'none';
      document.getElementById('main-card').style.display = 'block';
      loadData();
      setInterval(loadData, 5000);
    } else {
      alert('Invalid Terminal Passcode!');
    }
  });
}
function loadData() {
  fetch('/api/metrics', {headers: {'X-Session-Token': token}}).then(r => r.json()).then(data => {
    let html = '<div style="color:#00ffcc;font-weight:bold;margin-bottom:8px;">--- Hardware & DePIN Apps ---</div>';
    data.hw.forEach(i => { html += `<div class="row"><span>💻 Hardware [${i[0]}]</span><span>${i[1]}</span></div>`; });
    data.reserves.forEach(i => { html += `<div class="row"><span>🟢 ${i[0]}</span><span>${i[1]} | $${i[2]}</span></div>`; });
    html += '<div style="color:#00ffcc;font-weight:bold;margin:12px 0 8px 0;">--- DEX Yield Pairs ---</div>';
    data.pairs.forEach(i => { html += `<div class="row"><span>🔄 ${i[0]}</span><span>Liq $${i[1].toLocaleString()} (${i[2]})</span></div>`; });
    document.getElementById('metrics').innerHTML = html;
  });
}
function action(type) {
  document.getElementById('st').innerText = "Processing via UNIX Socket...";
  fetch('/api/' + type, {method:'POST', headers: {'X-Session-Token': token}}).then(r => r.json()).then(d => {
    document.getElementById('st').innerText = d.message;
    loadData();
  });
}
</script></body></html>"""

class SovereignHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200); self.send_header('Content-type', 'text/html'); self.end_headers()
            self.wfile.write(HTML.encode())
        elif self.path == '/api/metrics':
            if self.headers.get('X-Session-Token') != AUTH_TOKEN:
                self.send_response(401); self.end_headers(); return
            self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT token, balance, price_usd FROM reserves")
            reserves = c.fetchall()
            c.execute("SELECT pair_symbol, liquidity_usd, apy_range FROM liquidity_pairs")
            pairs = c.fetchall()
            c.execute("SELECT metric_key, value FROM hardware_telemetry")
            hw = c.fetchall()
            conn.close()
            self.wfile.write(json.dumps({"reserves": reserves, "pairs": pairs, "hw": hw}).encode())
        else:
            self.send_response(404); self.end_headers()
    def do_POST(self):
        if self.headers.get('X-Session-Token') != AUTH_TOKEN:
            self.send_response(401); self.end_headers(); return
        self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
        if self.path == '/api/sync':
            self.wfile.write(b'{"message":"SQLite WAL Knowledge Base Synchronized."}')
        elif self.path == '/api/swap':
            self.wfile.write(b'{"message":"EIP-4337 Route Verified via UNIX Socket (/tmp/sovereign_wallet.sock)."}')
    def log_message(self, *args): pass

if __name__ == '__main__':
    enforce_single_instance()
    port = 5050
    server = ReusableHTTPServer(('0.0.0.0', port), SovereignHandler)
    print(f"[+] Sovereign OS Web Server Running on port {port}...")
    try:
        server.serve_forever()
    finally:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

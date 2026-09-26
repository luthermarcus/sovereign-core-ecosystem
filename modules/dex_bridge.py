# Sovereign Core Production Plugin: P2P Tor DEX Socket Bridge
import subprocess
import socket
try:
    import socks
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False

PLUGIN_NAME = "DexTorBridge"
VERSION = "3.1.0"

def check_bridge_status():
    status_str = ""
    try:
        check = subprocess.run(["pgrep", "-f", "dex_daemon.py"], capture_output=True, text=True)
        if check.returncode == 0:
            status_str = "Status: Bridge Active (Port 8181 via Tor)"
        else:
            status_str = "Status: Bridge Offline (Daemon not running)"
    except:
        status_str = "Status: Bridge Diagnostic Failed"
        
    if SOCKS_AVAILABLE:
        status_str += " | Autonomous Tor Sync Enabled"
    else:
        status_str += " | Outbound Tor Sync Offline (Missing Dependency)"
        
    return status_str

def gossip_with_peer(target_onion, port=8181):
    if not SOCKS_AVAILABLE:
        return {"error": "python3-socks missing. Cannot route Tor."}
    try:
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15.0)
        s.connect((target_onion, port))
        s.sendall(b"PING")
        response = s.recv(2048).decode('utf-8')
        s.close()
        return {"status": "success", "response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(check_bridge_status())

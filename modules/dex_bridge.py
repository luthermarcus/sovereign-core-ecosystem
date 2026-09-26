# Sovereign Core Production Plugin: P2P Tor DEX Socket Bridge
import socket

PLUGIN_NAME = "DexTorBridge"
VERSION = "1.0.0"

def check_bridge_status():
    host = '127.0.0.1'
    port = 8181
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.close()
        return f"Status: Bridge Offline (Port {port} ready for Tor incoming)"
    except OSError:
        return f"Status: Bridge Active (Listening on {host}:{port} via Tor)"

if __name__ == "__main__":
    print(check_bridge_status())

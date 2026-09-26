import socket
import threading
import json
import os

def handle_peer(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        if "PING" in data:
            response = json.dumps({
                "status": "Active", 
                "node_type": "Sovereign Core DePIN", 
                "consensus": "SC-GPL Enforcement Active",
                "dex_version": "v2.20.0"
            })
            conn.sendall(response.encode('utf-8'))
    except Exception as e:
        pass
    finally:
        conn.close()

def start_dex_server():
    host = '127.0.0.1'
    port = 8181
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] Sovereign DEX Daemon listening silently on 127.0.0.1:{port}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_peer, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except Exception as e:
        print(f"[!] DEX Daemon Failed to Bind: {e}")

if __name__ == "__main__":
    start_dex_server()

import socket
import threading
import json
import os
import time
import sqlite3
import sys

# Ensure modules path is accessible
sys.path.append(os.path.expanduser("~/sovereign-core-ecosystem/modules"))
try:
    import dex_bridge
except ImportError:
    dex_bridge = None

def handle_peer(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        if "PING" in data:
            response = json.dumps({
                "status": "Active", 
                "node_type": "Sovereign Core DePIN", 
                "consensus": "SC-GPL Enforcement Active",
                "dex_version": "v2.24.0"
            })
            conn.sendall(response.encode('utf-8'))
    except Exception as e:
        pass
    finally:
        conn.close()

def autonomous_peer_sync():
    """Background thread that autonomously gossips with known Tor peers."""
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/knowledge.db")
    while True:
        try:
            if dex_bridge and dex_bridge.SOCKS_AVAILABLE:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                # Fetch known onion addresses (excluding placeholder)
                c.execute("SELECT onion_address FROM peer_network WHERE onion_address LIKE '%.onion' AND onion_address != 'pending_generation.onion'")
                peers = c.fetchall()
                
                for peer in peers:
                    target_onion = peer[0]
                    # Attempt background handshake over Tor
                    result = dex_bridge.gossip_with_peer(target_onion)
                    if "success" in result:
                        # Update last_seen timestamp on successful ping
                        conn.execute("UPDATE peer_network SET last_seen = CURRENT_TIMESTAMP WHERE onion_address = ?", (target_onion,))
                conn.commit()
                conn.close()
        except Exception:
            pass
        # Sleep for 5 minutes before the next autonomous sync
        time.sleep(300)

def start_dex_server():
    host = '127.0.0.1'
    port = 8181
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Spawn the autonomous sync thread
    sync_thread = threading.Thread(target=autonomous_peer_sync)
    sync_thread.daemon = True
    sync_thread.start()
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] Sovereign DEX Daemon & Autonomous Sync listening on 127.0.0.1:{port}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_peer, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except Exception as e:
        print(f"[!] DEX Daemon Failed to Bind: {e}")

if __name__ == "__main__":
    start_dex_server()

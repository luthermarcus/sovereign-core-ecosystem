import sqlite3
import os
import subprocess

PLUGIN_NAME = "TorPeerDiscovery"
VERSION = "2.1.0"

def execute_audit():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/knowledge.db")
    status = "Active"
    onion_address = "Pending Tor v3 Generation"
    
    try:
        if os.path.exists("/var/lib/tor/sovereign_dex_p2p/hostname"):
            with open("/var/lib/tor/sovereign_dex_p2p/hostname", "r") as f:
                onion_address = f.read().strip()
        else:
            status = "Standby (Awaiting Tor configuration)"
    except PermissionError:
        status = "Restricted (Requires sudo verification)"

    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("CREATE TABLE IF NOT EXISTS peer_network (onion_address TEXT PRIMARY KEY, last_seen DATETIME)")
        conn.execute("INSERT OR REPLACE INTO peer_network (onion_address, last_seen) VALUES (?, CURRENT_TIMESTAMP)", (onion_address,))
        conn.commit()
        conn.close()
    except:
        pass
        
    return f"Status: Native P2P Discovery {status} ({onion_address})"

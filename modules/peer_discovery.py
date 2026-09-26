# Sovereign Core Beta Plugin: DePIN Peer Discovery Auditor
import socket

PLUGIN_NAME = "PeerDiscovery"
VERSION = "1.2.0"

def execute_audit():
    ports = [4449, 9050]
    active = 0
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex(("127.0.0.1", p)) == 0:
                active += 1
            s.close()
        except:
            pass
    return f"Status: {active}/{len(ports)} DePIN/Tor Sockets Active"

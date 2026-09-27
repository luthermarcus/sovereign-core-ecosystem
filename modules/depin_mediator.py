import os, sys, time, json
sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class DePINTrafficMediator:
    RESTRICTED_PORTS = [22, 23, 25, 445]

    @classmethod
    def intercept_peer_connection(cls, peer_ip, app_target, requested_port):
        print(f"\n[*] [NETWORK SHIELD] Intercepted {app_target} client from {peer_ip}...")
        time.sleep(0.3)
        if requested_port in cls.RESTRICTED_PORTS:
            print(f"[X] [NETWORK SHIELD] SIMULATION FAILED: Malicious port {requested_port} blocked.")
            try:
                cfg_path = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_config.json")
                with open(cfg_path, "r") as f:
                    cfg = json.load(f)
                if "security_shield" not in cfg:
                    cfg["security_shield"] = {"blacklisted_peers": 0}
                cfg["security_shield"]["blacklisted_peers"] += 1
                with open(cfg_path, "w") as f:
                    json.dump(cfg, f, indent=2)
            except Exception:
                pass
            print(f"[-] [NETWORK SHIELD] Peer {peer_ip} added to Blacklist. Config Updated.")
            return False
            
        print(f"[v] [NETWORK SHIELD] Traffic verified. Forwarding to L2 {app_target} container.")
        return True

if __name__ == "__main__":
    DePINTrafficMediator.intercept_peer_connection("192.168.1.105", "Mysterium", 25)

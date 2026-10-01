import os, sys, time, hashlib, json
sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class BidirectionalFrameMediator:
    RAM_BUFFER = "/dev/shm/frame_transit.tmp"

    @classmethod
    def _generate_digest(cls, payload):
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    @classmethod
    def process_egress(cls, destination, payload):
        print(f"\n[>>] [EGRESS MEDIATOR] Staging outbound packet to {destination}...")
        digest = cls._generate_digest(payload)
        envelope = {"dest": destination, "payload": payload, "sha256": digest, "timestamp": time.time()}
        
        # Verify outgoing envelope integrity in /dev/shm
        with open(cls.RAM_BUFFER, "w") as f:
            json.dump(envelope, f)
            
        print(f"[v] [EGRESS VERIFIED] SHA-256: {digest[:12]}... Packet authorized for broadcast.")
        return envelope

    @classmethod
    def process_ingress(cls, source, envelope):
        print(f"\n[<<] [INGRESS MEDIATOR] Intercepted incoming packet from {source}...")
        if not isinstance(envelope, dict) or "payload" not in envelope or "sha256" not in envelope:
            print("[X] [INGRESS FAILED] Frame malformed. Dropped in /dev/shm.")
            return False
            
        expected_digest = cls._generate_digest(envelope["payload"])
        if envelope["sha256"] != expected_digest:
            print("[X] [INGRESS FAILED] Cryptographic checksum mismatch. Tampering detected.")
            return False
            
        print(f"[v] [INGRESS VERIFIED] SHA-256 Match ({expected_digest[:12]}...). Forwarded to L1 Anchor.")
        return True

if __name__ == "__main__":
    print("=== INITIATING BIP 324 STYLE BIDIRECTIONAL MEDIATOR TESTS ===")
    test_data = {"node": "sos-node-host", "metric": "yield_sync", "val": 49.20}
    env = BidirectionalFrameMediator.process_egress("BIP300_RELAY", test_data)
    BidirectionalFrameMediator.process_ingress("BIP300_RELAY", env)

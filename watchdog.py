import os, time, json
from three_prong_shield import verify_three_prong_interlock
def run_watchdog():
    print("[*] Sovereign Core OS Watchdog v7.67.0-beta online. Monitoring /dev/shm intent ring...")
    os.makedirs("/dev/shm", exist_ok=True)
    while True:
        ring_path = "/dev/shm/dex_intent_ring.tmp"
        if os.path.exists(ring_path):
            try:
                with open(ring_path, "r") as f: content = f.read().strip()
                if content:
                    payload = json.loads(content)
                    valid, reason = verify_three_prong_interlock(payload)
                    print(f"[v] {reason}" if valid else f"[!] SECURITY INTERLOCK TRIGGERED: {reason}")
                    os.remove(ring_path)
            except Exception as e: print(f"[!] Watchdog read error: {e}")
        time.sleep(5)
if __name__ == "__main__": run_watchdog()

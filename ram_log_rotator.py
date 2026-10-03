import os
import time

def rotate_logs():
    print("[*] Executing RAM WAL log rotation and memory purge sweep...")
    log_files = [
        "/dev/shm/web_dashboard.log",
        "/dev/shm/liquidity_daemon.log",
        "/dev/shm/earnings_aggregator.log"
    ]
    
    for log in log_files:
        if os.path.exists(log):
            size = os.path.getsize(log)
            if size > 1024 * 1024:  # Rotate if greater than 1MB
                with open(log, "w") as f:
                    f.write("[TRUNCATED] Log rotated by Sovereign Core RAM Rotator.\n")
                print(f"[✓] Rotated oversized log: {log}")
            else:
                print(f"[✓] Log file {log} within safe size limits ({size} bytes).")

if __name__ == "__main__":
    rotate_logs()

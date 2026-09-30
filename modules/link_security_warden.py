import os, sys, time, json, sqlite3, hashlib
sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class LinkSecurityWarden:
    TRUST_STORE = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")
    TARGET_SHM = "/dev/shm"

    @classmethod
    def audit_and_sanitize_links(cls):
        print("\n[*] [LINK WARDEN] Scanning and tracking system links for symlink vectors and anomalies...")
        time.sleep(0.2)
        
        # Audit files in /dev/shm for symlink hazards
        quarantine_count = 0
        monitored_links = []
        for filename in os.listdir(cls.TARGET_SHM):
            filepath = os.path.join(cls.TARGET_SHM, filename)
            if os.path.islink(filepath):
                print(f"[!] [WARNING] Symbolic link detected in secure RAM buffer: {filepath}. Purging...")
                os.unlink(filepath)
                quarantine_count += 1
            elif "system_link" in filename or "bridge" in filename or "state" in filename:
                monitored_links.append(filename)

        audit_status = {
            "warden_status": "ACTIVE_LINK_SANITIZATION",
            "symlinks_purged": quarantine_count,
            "active_secure_links": len(monitored_links),
            "timestamp": time.time(),
            "warden_hash": hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        }
            
        conn = sqlite3.connect(cls.TRUST_STORE)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("CREATE TABLE IF NOT EXISTS link_warden_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, purged INTEGER, warden_hash TEXT, timestamp REAL)")
        conn.execute("INSERT INTO link_warden_audit (purged, warden_hash, timestamp) VALUES (?, ?, ?)", 
                     (quarantine_count, audit_status["warden_hash"], time.time()))
        conn.commit()
        conn.close()
        
        print(f"[v] [LINK WARDEN] Audit complete. Purged: {quarantine_count} | Warden Hash: {audit_status['warden_hash']}")
        return True

if __name__ == "__main__":
    LinkSecurityWarden.audit_and_sanitize_links()

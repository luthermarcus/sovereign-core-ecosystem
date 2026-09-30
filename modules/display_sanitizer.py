import os, sys, time, json, sqlite3, hashlib
sys.path.insert(0, os.path.expanduser("~/sovereign-core-ecosystem"))

class DisplaySanitizer:
    TRUST_STORE = os.path.expanduser("~/sovereign-core-ecosystem/trust_store.db")
    SANITIZER_MEM = "/dev/shm/display_sanitizer_state.tmp"

    @classmethod
    def sanitize_viewport(cls):
        print("\n[*] [SANITIZER] Purging terminal overlap artifacts and resetting ANSI viewport coordinates...")
        time.sleep(0.2)
        
        # Hard reset ANSI screen buffer and cursor position
        sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
        sys.stdout.flush()
        
        sanitizer_state = {
            "sanitizer_status": "TERMINAL_BUFFER_SANITISED",
            "ansi_sequence": "ESC[H ESC[2J ESC[3J",
            "timestamp": time.time(),
            "sanitizer_hash": hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        }
        
        with open(cls.SANITIZER_MEM, "w") as f:
            json.dump(sanitizer_state, f, indent=2)
            
        conn = sqlite3.connect(cls.TRUST_STORE)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("CREATE TABLE IF NOT EXISTS display_sanitizer_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT, sanitizer_hash TEXT, timestamp REAL)")
        conn.execute("INSERT INTO display_sanitizer_audit (status, sanitizer_hash, timestamp) VALUES (?, ?, ?)", 
                     (sanitizer_state["sanitizer_status"], sanitizer_state["sanitizer_hash"], time.time()))
        conn.commit()
        conn.close()
        
        print(f"[v] [SANITIZER] Viewport successfully sanitized. Sanitizer Hash: {sanitizer_state['sanitizer_hash']}")
        return True

if __name__ == "__main__":
    DisplaySanitizer.sanitize_viewport()

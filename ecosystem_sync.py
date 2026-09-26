# Sovereign Core Production Utility: Local Ingestion & File Indexer
import os
import sqlite3
import hashlib

def scan_and_index():
    home_dir = os.path.expanduser("/home/luther")
    eco_dir = os.path.expanduser("~/sovereign-core-ecosystem")
    db_path = os.path.join(eco_dir, "knowledge.db")
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS local_file_registry (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_path TEXT,
            file_size INTEGER,
            sha256_hash TEXT,
            scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    indexed_count = 0
    for root, dirs, files in os.walk(home_dir):
        # Skip virtualenvs and hidden git caches to save I/O
        if ".git" in root or "venv" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith((".py", ".sh", ".db", ".md")):
                fpath = os.path.join(root, file)
                try:
                    size = os.path.getsize(fpath)
                    with open(fpath, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    conn.execute("""
                        INSERT OR REPLACE INTO local_file_registry (file_name, file_path, file_size, sha256_hash)
                        VALUES (?, ?, ?, ?)
                    """, (file, fpath, size, file_hash))
                    indexed_count += 1
                except Exception:
                    pass
                    
    conn.commit()
    conn.close()
    print(f"[v] Ecosystem Sync Complete: Successfully indexed {indexed_count} local files into knowledge.db.")

if __name__ == "__main__":
    scan_and_index()

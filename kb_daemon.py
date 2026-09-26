import os
import sqlite3
import hashlib

DB_PATH = "/home/luther/sovereign-core-ecosystem/knowledge.db"
VAULT_DIR = "/home/luther/sovereign-core-ecosystem/knowledge_vault"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            path TEXT,
            content TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(
            path,
            content,
            content='entries',
            content_rowid='rowid'
        )
    """)
    conn.commit()
    return conn

def ingest_vault():
    conn = init_db()
    for root, _, files in os.walk(VAULT_DIR):
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                with open(full_path, "r", encoding="utf-8") as file:
                    content = file.read()
                file_id = hashlib.md5(full_path.encode()).hexdigest()
                conn.execute(
                    "REPLACE INTO entries (id, path, content) VALUES (?, ?, ?)",
                    (file_id, full_path, content)
                )
    conn.execute("INSERT INTO entries_fts(entries_fts) VALUES('rebuild')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    ingest_vault()

import sqlite3, sys

print(f"Python {sys.version_info.major}.{sys.version_info.minor} active | SQLite {sqlite3.sqlite_version}")

conn = sqlite3.connect("pixel_telemetry.db")
cursor = conn.cursor()

# Apply XDA-recommended performance flags for mobile flash storage
cursor.execute("PRAGMA journal_mode=WAL;")
cursor.execute("PRAGMA synchronous=NORMAL;")
cursor.execute("PRAGMA cache_size=-2000;") # ~2MB cache

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Active Tables:", cursor.fetchall())
print("Journal Mode:", cursor.execute("PRAGMA journal_mode;").fetchone()[0])

conn.close()
print("[+] SQLite mobile telemetry storage optimized successfully.")

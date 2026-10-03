import sqlite3
conn = sqlite3.connect("pixel_telemetry.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY, status TEXT)")
cursor.execute("INSERT INTO metrics (status) VALUES ('Operational')")
conn.commit()
cursor.execute("SELECT * FROM metrics")
print(cursor.fetchall())
conn.close()

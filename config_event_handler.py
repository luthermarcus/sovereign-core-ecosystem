"""Sovereign Core OS - State-Change Deduplication & Governance Event Ledger"""
import time
from sos_platform import connect_wal_db

def record_governance_event(event_type: str, detail: str):
    conn = connect_wal_db("trust_store.db")
    conn.execute("CREATE TABLE IF NOT EXISTS gov_events (ts REAL, event_type TEXT, detail TEXT);")
    conn.execute("INSERT INTO gov_events VALUES (?, ?, ?);", (time.time(), event_type, detail))
    conn.commit()
    conn.close()
    return True

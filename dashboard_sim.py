import os, sqlite3, json

def get_ecosystem_status():
    db_path = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db")
    if not os.path.exists(db_path):
        return {"status": "STANDBY", "nodes": 0, "treasury_balance": 0.0}
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        nodes = cursor.execute("SELECT COUNT(*) FROM depin_throughput").fetchone()[0]
    except:
        nodes = 0
    conn.close()
    return {"status": "PRE_LIVE_BETA_v7.47.0", "active_nodes": nodes, "dao_lock": "ENABLED"}

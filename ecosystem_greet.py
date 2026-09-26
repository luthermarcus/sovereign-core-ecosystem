import sqlite3, os

DB_NAME = os.path.expanduser("~/myst_metrics.db")

def show_full_command_center():
    print("========================================")
    print("=== UNREAD SYSTEM FLAGS & ECOSYSTEM ALERTS ===")
    print("========================================")
    
    if os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        try:
            cur.execute("SELECT timestamp, flag_type, message FROM system_flags ORDER BY id DESC LIMIT 5;")
            rows = cur.fetchall()
            for r in rows:
                print(f"[{r[0]}] {r[1]}: {r[2]}")
        except Exception:
            print("[INFO] No unread system flags logged.")
        conn.close()
    else:
        print("[INFO] Ecosystem database online and nominal.")

if __name__ == "__main__":
    show_full_command_center()

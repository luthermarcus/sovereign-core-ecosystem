import os
import json
import hashlib
import sqlite3
import time

class OSStateRollup:
    IPC_PATH = "/dev/shm/l2_state_root.json"
    DB_PATH = os.path.expanduser("~/sovereign-core-ecosystem/sys_health.db")

    @classmethod
    def execute_rollup_to_l1(cls, l2_virtual_flags):
        """
        Acts as an L2 Rollup: Batches virtual flags, generates a SHA-256 state root,
        and settles the hash onto the Native Host (L1) memory and disk.
        """
        # Read Native Host L1 Hardware State
        l1_state = {"kernel": os.uname().release, "load": "unknown", "thermal": "unknown"}
        try:
            with open("/proc/loadavg", "r") as f: l1_state["load"] = f.read().split()[0]
        except Exception: pass
        
        # Combine states and calculate Cryptographic Root
        combined_state = {"l1_base": l1_state, "l2_rollup": l2_virtual_flags, "timestamp": time.time()}
        serialized_state = json.dumps(combined_state, sort_keys=True).encode()
        state_root_hash = hashlib.sha256(serialized_state).hexdigest()
        
        payload = {
            "state_root": state_root_hash,
            "l1_base_status": "Anchored",
            "l2_rollup_status": "Synchronized",
            "payload": combined_state
        }
        
        # Settle to fast L1 RAM (/dev/shm)
        try:
            with open(cls.IPC_PATH, "w") as f:
                json.dump(payload, f)
        except Exception: pass
        
        # Settle to immutable L1 Disk (SQLite WAL)
        try:
            conn = sqlite3.connect(cls.DB_PATH)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute('''
                CREATE TABLE IF NOT EXISTS l2_state_anchors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    state_root TEXT,
                    l2_flag_count INTEGER
                )
            ''')
            conn.execute("INSERT INTO l2_state_anchors (state_root, l2_flag_count) VALUES (?, ?)", 
                         (state_root_hash, len(l2_virtual_flags)))
            conn.commit()
            conn.close()
        except Exception: pass
        
        return payload

    @classmethod
    def read_l1_anchor(cls):
        try:
            with open(cls.IPC_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return {"state_root": "0x0000... (Awaiting Sync)", "l1_base_status": "Standby", "l2_rollup_status": "Standby"}

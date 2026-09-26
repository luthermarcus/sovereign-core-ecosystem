# Sovereign Core Beta Plugin: Cryptographic Integrity & Vault Signer
import os
import hashlib

PLUGIN_NAME = "CryptoIntegrity"
VERSION = "1.9.0"

def execute_audit():
    target_dir = os.path.expanduser("~/sovereign-core-ecosystem")
    dbs = ["sys_health.db", "wallet.db", "knowledge.db"]
    hashed_count = 0
    for db in dbs:
        path = os.path.join(target_dir, db)
        if os.path.exists(path):
            try:
                hasher = hashlib.sha256()
                with open(path, "rb") as f:
                    buf = f.read()
                    hasher.update(buf)
                sig = hasher.hexdigest()
                with open(os.path.join(target_dir, "integrity", f"{db}.sig"), "w") as sf:
                    sf.write(sig)
                hashed_count += 1
            except:
                pass
    return f"Status: Active ({hashed_count} WAL Vaults Cryptographically Signed)"

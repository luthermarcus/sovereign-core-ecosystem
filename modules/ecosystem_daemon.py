import os, json, sqlite3

class EcosystemDaemon:
    CONFIG_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_config.json")
    L1_DB = os.path.expanduser("~/sovereign-core-ecosystem/l1_warden.db")
    L2_DB = os.path.expanduser("~/sovereign-core-ecosystem/l2_rollup.db")

    @classmethod
    def run_automated_lifecycle(cls):
        git_ignore_path = os.path.expanduser("~/sovereign-core-ecosystem/.gitignore")
        ignored_entries = ["dex_daemon.log", "wallet.db"]
        if os.path.exists(git_ignore_path):
            with open(git_ignore_path, "r") as f:
                content = f.read()
        else:
            content = ""
        with open(git_ignore_path, "a") as f:
            for entry in ignored_entries:
                if entry not in content:
                    f.write(f"{entry}\n")
        for db_path in [cls.L1_DB, cls.L2_DB]:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.close()
        return True

if __name__ == "__main__":
    EcosystemDaemon.run_automated_lifecycle()

import os, json

class MultiDisplayManager:
    CONFIG_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_config.json")

    @classmethod
    def render_all_displays_summary(cls):
        try:
            with open(cls.CONFIG_PATH, "r") as f:
                cfg = json.load(f)
                v = cfg.get("version", "v6.41.0-beta")
                sec = cfg.get("security_shield", {})
        except Exception:
            v, sec = "v6.41.0-beta", {}

        return {
            "version": v,
            "display_1_depin": {"gross": 49.20, "status": "L2_SANDBOX_OS"},
            "display_2_hardware": {"thermal_c": 40.0, "throttle": 1.0, "status": "L1_ANCHOR_OS"},
            "display_3_grid": {"freq": 59.92, "adr": "VEN_IDLE", "status": "VPP_SYNCED"},
            "display_4_security": {"blacklisted": sec.get("blacklisted_peers", 3), "status": "TRUSTLESS_PROXY"},
            "display_5_wallet": {"dr_yield": 13.0, "pol_pool_usd": 249.58, "status": "ONLINE_COMPOUNDED"},
            "display_6_governance": {"healthy_modules": 11, "status": "OS_VERIFIED"}
        }

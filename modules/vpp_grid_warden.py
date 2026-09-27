import os, time, json, random

class VPPGridWarden:
    CONFIG_PATH = os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_config.json")

    @classmethod
    def simulate_grid_telemetry(cls):
        # Simulate grid frequency (Normal = ~60.0Hz, Stress < 59.95Hz)
        base_freq = 60.0
        fluctuation = random.uniform(-0.08, 0.02)
        current_freq = round(base_freq + fluctuation, 3)
        
        openadr_signal = "VEN_IDLE"
        dr_multiplier = 1.0
        performance_credit_usd = 0.0

        if current_freq < 59.95:
            openadr_signal = "VEN_CURTAIL_RRS"
            dr_multiplier = 0.1 # Instant ancillary load shedding
            performance_credit_usd = 0.50 # Earned DR incentive for shedding load

        with open(cls.CONFIG_PATH, "r") as f:
            cfg = json.load(f)

        if "vpp_grid" not in cfg:
            cfg["vpp_grid"] = {"dr_capacity_credits_usd": 12.50, "dr_performance_credits_usd": 0.0}

        cfg["vpp_grid"]["grid_frequency_hz"] = current_freq
        cfg["vpp_grid"]["openadr_status"] = openadr_signal
        
        if performance_credit_usd > 0:
            cfg["vpp_grid"]["dr_performance_credits_usd"] += performance_credit_usd

        # Override hardware warden if grid demands emergency curtailment
        if openadr_signal != "VEN_IDLE":
            if "hardware_warden" not in cfg:
                cfg["hardware_warden"] = {}
            cfg["hardware_warden"]["predictive_throttle_multiplier"] = dr_multiplier

        cfg["version"] = "v6.32.0-beta"
        
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)

if __name__ == "__main__":
    VPPGridWarden.simulate_grid_telemetry()

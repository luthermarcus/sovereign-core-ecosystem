#!/usr/bin/env python3
"""Sovereign Core OS (SOS) - Universal Terminal & DAO Greeting Banner"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sos_platform import get_host_info, get_ram_ledger_dir, load_local_profile

profile = load_local_profile()
host = get_host_info()
in_ip = host["inbound_ip"]
out_ip = host["outbound_ip"]
native_os = host["os"]
lock_dir = get_ram_ledger_dir()

vault_addr = profile.get("vault_display", "0xFOX_SOVEREIGN_VAULT")
app_count = profile.get("active_depin_count", 7)
pol_yield = profile.get("pol_yield_display", "$0.00")

lock_file = os.path.join(lock_dir, f"sos_greet_{os.getuid() if hasattr(os, 'getuid') else 'u'}.stamp")
if not os.environ.get("SOS_FORCE_GREET"):
    try:
        if os.path.exists(lock_file) and (time.time() - os.path.getmtime(lock_file)) < 3.0:
            sys.exit(0)
        with open(lock_file, "w") as lf:
            lf.write(str(time.time()))
    except Exception:
        pass

def get_temp():
    for zone in ("/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"):
        if os.path.exists(zone):
            try:
                with open(zone, "r") as tf:
                    return f"{int(tf.read().strip()) / 1000.0:.1f}°C"
            except Exception:
                pass
    return "Nominal"

ip_display = f"{in_ip}->{out_ip}" if in_ip != out_ip else out_ip

print(f"\n🦊 Sovereign Core OS Native Dash | Active Apps: {app_count} | POL Yield: {pol_yield} | In:{in_ip} Out:{out_ip}")
print(f"""
+---------------------------------------------------------------------+
| FOX SOVEREIGN CORE OS - NATIVE HOST TERMINAL & DAO DASHBOARD        |
+---------------------------------------------------------------------+
| [*] Consensus: AuxPoW (Merged Mining)  | In/Out: {ip_display:<19}|
| [*] Thermal Guard: Stable ({get_temp()})     | Native OS: {native_os:<16}|
| [*] Active DePIN Apps: {app_count:<15} | POL Yield: {pol_yield:<16}|
| [*] L2 Vault Address: {vault_addr:<16} | Bridge: Boomerang (Δt)     |
+---------------------------------------------------------------------+
| RUN SHORTCUTS:                                                      |
|   dash     : Launch Interactive 6-Tab TUI (Wallets, SEC, Thermals)  |
|   earnings : Legacy Portfolio Display (Python flag -1)              |
|   ai-diag  : Mobile Termux/Shizuku edge diagnostics script          |
+---------------------------------------------------------------------+""")

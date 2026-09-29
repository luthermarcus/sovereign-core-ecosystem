import os
from modules.l2_state_rollup import OSStateRollup
def render_dashboard_four():
    anchor = OSStateRollup.read_l1_anchor()
    root = anchor.get('state_root', '0000')
    root_hash = root if root.startswith("0x") else f"0x{root[:24]}"
    thermal = anchor.get('thermal_health', 'Awaiting Sync')
    
    print("=" * 70 + "\n=== DASHBOARD 4: L1/L2 CROSS-OS STATE ROLLUP FLAGS ===\n" + "=" * 70)
    print(f"  [FLAG] L1_HOST_KERNEL    : {os.uname().release}")
    print(f"  [FLAG] L1_THERMAL_WARDEN : {thermal}")
    print(f"  [FLAG] L2_ROLLUP_STATUS  : {anchor.get('l2_status', 'Standby')}")
    print(f"  [>] Anchored State Root  : {root_hash}...\n" + "=" * 70)
if __name__ == "__main__": render_dashboard_four()

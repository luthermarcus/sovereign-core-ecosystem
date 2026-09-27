import os, sys, argparse, time
from modules.display_manager import MultiDisplayManager

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')

def cli_grid_audit():
    clear_screen()
    res = MultiDisplayManager.render_all_displays_summary()
    vpp = res.get('vpp_raw', {'grid_frequency_hz': 60.0, 'openadr_status': 'VEN_IDLE', 'dr_capacity_credits_usd': 12.50, 'dr_performance_credits_usd': 0.0})
    print("=== VIRTUAL POWER PLANT & DEMAND RESPONSE AUDIT ===\n" + "=" * 70)
    print(f"  Local Grid Frequency  : {vpp['grid_frequency_hz']} Hz")
    print(f"  OpenADR 2.0b Status   : {vpp['openadr_status']}")
    print("-" * 70)
    print(f"  DR Capacity Payments  : ${vpp['dr_capacity_credits_usd']:.2f} USD")
    print(f"  DR Performance Yield  : ${vpp['dr_performance_credits_usd']:.2f} USD")
    print("=" * 70)

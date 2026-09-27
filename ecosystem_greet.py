from modules.display_manager import MultiDisplayManager
def main():
    res = MultiDisplayManager.render_all_displays_summary()
    v = res["version"]
    print("=" * 75)
    print(f"=== SOVEREIGN CORE OS {v} : ALL 6 DISPLAYS ACTIVE ===")
    print("=" * 75)
    d1, d2, d3 = res["display_1_depin"], res["display_2_hardware"], res["display_3_grid"]
    d4, d5, d6 = res["display_4_security"], res["display_5_wallet"], res["display_6_governance"]
    print(f"  [Display 1] DePIN Yield      : ${d1['gross']} USD [{d1['status']}]")
    print(f"  [Display 2] Power & Warden   : {d2['thermal_c']}°C | L2 Throttle: {d2['throttle']}x [{d2['status']}]")
    print(f"  [Display 3] VPP Grid (ADR)   : {d3['freq']}Hz | Signal: {d3['adr']} [{d3['status']}]")
    print(f"  [Display 4] Security Guard   : L1 Kernel Secure | L2 Isolated [{d4['status']}]")
    print(f"  [Display 5] Wallet & Reserves: DR Credits: ${d5['dr_yield']} | POL: ${d5['pol_pool_usd']} [{d5['status']}]")
    print(f"  [Display 6] Governance & Node: Orphans Tracked ({d6['orphans']}) [{d6['status']}]")
    print("=" * 75)
    print("  >>> Type 'sos' for Master TUI or 'sos --grid' for VPP audit. <<<")
if __name__ == "__main__":
    main()

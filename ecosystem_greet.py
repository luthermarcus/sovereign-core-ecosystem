from modules.display_manager import MultiDisplayManager
def main():
    res = MultiDisplayManager.render_all_displays_summary()
    print("=" * 70)
    print("=== SOVEREIGN CORE OS v6.17.0-beta : ALL 5 DISPLAYS ACTIVE ===")
    print("=" * 70)
    d1 = res["display_1_depin"]
    d2 = res["display_2_hardware"]
    d3 = res["display_3_consensus"]
    d4 = res["display_4_security"]
    d5 = res["display_5_governance"]
    print(f"  [Display 1] DePIN Yield      : ${d1['gross']} USD | POL Tax: ${d1['pol_tax']} [{d1['status']}]")
    print(f"  [Display 2] Hardware Warden  : {d2['thermal_c']}°C | /dev/shm: {d2['shm_mb']} MB [{d2['status']}]")
    print(f"  [Display 3] Sidechain (BIP300) : Drivechain Active | BMM: Ready [{d3['status']}]")
    print(f"  [Display 4] Security Guard   : L1 Kernel Secure | L2 Isolated [{d4['status']}]")
    print(f"  [Display 5] Governance       : Orphans Tracked ({len(d5['orphen'] if 'orphen' in d5 else d5['orphans'])}) [{d5['status']}]")
    print("=" * 70)
    print("  >>> Type 'sos' for Master TUI or 'sos --depin' for direct audit. <<<")
if __name__ == "__main__":
    main()

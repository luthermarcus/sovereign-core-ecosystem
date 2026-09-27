from modules.display_manager import MultiDisplayManager

def main():
    res = MultiDisplayManager.render_all_displays_summary()
    print("=" * 70)
    print("=== SOVEREIGN CORE OS v6.14.0-beta : ALL 4 DISPLAYS ACTIVE ===")
    print("=" * 70)
    d1 = res["display_1_depin"]
    d2 = res["display_2_hardware"]
    d3 = res["display_3_consensus"]
    d4 = res["display_4_security"]

    print(f"  [Display 1] DePIN Stack Yield : ${d1['gross']} USD \vert{} POL Tax:${d1['pol_tax']} [{d1['status']}]")
    print(f"  [Display 2] Hardware Warden  : {d2['thermal_c']}°C | /dev/shm: {d2['shm_mb']} MB [{d2['status']}]")
    print(f"  [Display 3] Sidechain (BIP300) : Drivechain Active | BMM: Ready [{d3['status']}]")
    print(f"  [Display 4] Security Guard   : L1 Kernel Secure | L2 Isolated [{d4['status']}]")
    print("=" * 70)
    print("  >>> Type 'sos' for TUI menu or 'sos --depin' for direct audit. <<<\n")

if __name__ == "__main__":
    main()

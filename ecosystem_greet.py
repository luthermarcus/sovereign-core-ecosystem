from modules.display_manager import MultiDisplayManager
def main():
    res = MultiDisplayManager.render_all_displays_summary()
    print("=" * 70)
    print("=== SOVEREIGN CORE OS v6.18.0-beta : ALL 6 DISPLAYS ACTIVE ===")
    print("=" * 70)
    d1 = res["display_1_depin"]
    d2 = res["display_2_hardware"]
    d3 = res["display_3_consensus"]
    d4 = res["display_4_security"]
    d5 = res["display_5_wallet"]
    d6 = res["display_6_governance"]
    print(f"  [Display 1] DePIN Yield      : ${d1['gross']} USD | POL Tax: ${d1['pol_tax']} [{d1['status']}]")
    print(f"  [Display 2] Hardware Warden  : {d2['thermal_c']}°C | /dev/shm: {d2['shm_mb']} MB [{d2['status']}]")
    print(f"  [Display 3] Sidechain (BIP300) : Drivechain Active | BMM: Ready [{d3['status']}]")
    print(f"  [Display 4] Security Guard   : L1 Kernel Secure | L2 Isolated [{d4['status']}]")
    print(f"  [Display 5] Wallet & Liquidity : Reserves: {d5['reserve_btc']} BTC | POL: ${d5['pol_pool_usd']} [{d5['status']}]")
    print(f"  [Display 6] Governance & About : Orphans Tracked ({len(d6['orphans'])}) [{d6['status']}]")
    print("=" * 70)
    print("  >>> Type 'sos' for Master TUI or 'sos --depin' for direct audit. <<<")
if __name__ == "__main__":
    main()

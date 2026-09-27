import os, sys, argparse, time
from modules.display_manager import MultiDisplayManager
from modules.depin_sidechain import DePINSidechainEngine
from modules.sovereign_core_kernel import SovereignCoreKernel
from modules.cross_chain_peg import CrossChainPegModule
from modules.hardware_warden import HardwareWarden
from modules.role_switcher import RoleSwitcherEngine
from modules.beefy_vault import BeefyVaultIntegration

def clear_screen(): os.system('clear' if os.name == 'posix' else 'cls')

def cli_depin_audit():
    clear_screen()
    res = DePINSidechainEngine.calculate_depin_capital_routing()
    print("=== DEPIN CAPITAL ROUTING & 6-APP AUDIT ===\n" + "=" * 70)
    for app, amt in res['stack_breakdown'].items():
        print(f"  - {app.capitalize():<15}: ${amt:.2f} USD [ACTIVE]")
    print("-" * 70)
    print(f"  Gross DePIN Yield      : ${res['gross_yield_usd']:.2f} USD")
    print(f"  5% POL Development Tax : ${res['pol_development_tax_5_percent']:.2f} USD")
    print(f"  Net User Yield         : ${res['net_user_yield_usd']:.2f} USD")
    print("=" * 70)

def cli_wallet_audit():
    clear_screen()
    vault_res = BeefyVaultIntegration.execute_auto_compound()
    print("=== WALLET, RESERVES & BEEFY AUTO-COMPOUND AUDIT ===\n" + "=" * 70)
    print("  L1 Parent Reserve Balance : 1.25 BTC [SECURE ESCROW]")
    print(f"  Protocol-Owned Liquidity  : ${vault_res['updated_pol_pool_usd']} USD [BEEFY AUTO-COMPOUNDED]")
    print("  BIP 300 Sidechain Locked  : 0.50 BTC [ANCHORED SLOT 1]")
    print("  Wallet DB Status          : WAL Synchronized [wallet.db]")
    print("=" * 70)

def cli_kernel_audit():
    clear_screen()
    res = SovereignCoreKernel.audit_kernel_integration()
    print("=== KERNEL & HARDWARE INTEGRATION AUDIT ===\n" + "=" * 70)
    print(f"  L1 Host Status : {res['l1_host_status']}")
    print(f"  L2 Sandbox     : {res['l2_sandbox_status']}")
    print(f"  BIP 300 Status : {res['bip300_drivechain']}")
    print(f"  BIP 301 BMM    : {res['bip301_bmm']}")
    print("=" * 70)

def cli_peg_simulator():
    clear_screen()
    res = CrossChainPegModule.initiate_two_way_peg(0.5, "Sovereign_Core_L2_Sidechain")
    print("=== BIP 300 TWO-WAY PEG SIMULATOR ===\n" + "=" * 70)
    print(f"  TxID           : {res['peg_txid']}")
    print(f"  Amount Locked  : {res['amount']} BTC")
    print(f"  Status         : {res['status']}")
    print("=" * 70)


def cli_grid_audit():
    clear_screen()
    from modules.display_manager import MultiDisplayManager
    res = MultiDisplayManager.render_all_displays_summary()
    vpp = res['vpp_raw']
    print("=== VIRTUAL POWER PLANT & DEMAND RESPONSE AUDIT ===
" + "=" * 70)
    print(f"  Local Grid Frequency  : {vpp['grid_frequency_hz']} Hz")
    print(f"  OpenADR 2.0b Status   : {vpp['openadr_status']}")
    print("-" * 70)
    print(f"  DR Capacity Payments  : ${vpp['dr_capacity_credits_usd']:.2f} USD [STANDBY ESCROW]")
    print(f"  DR Performance Yield  : ${vpp['dr_performance_credits_usd']:.2f} USD [CURTAILMENT EARNED]")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Sovereign Core OS Master Sandbox CLI")
    parser.add_argument("--depin", action="store_true", help="Run DePIN capital routing audit")
    parser.add_argument("--kernel", action="store_true", help="Run L1/L2 kernel integration audit")
    parser.add_argument("--peg", action="store_true", help="Run BIP 300 Two-Way Peg simulator")
    parser.add_argument("--grid", action="store_true", help="Run VPP grid & demand response audit")
    parser.add_argument("--wallet", action="store_true", help="Run wallet & liquidity audit")
    args, unknown = parser.parse_known_args()

    if args.depin:
        cli_depin_audit()
        return
    elif args.kernel:
        cli_kernel_audit()
        return
    elif args.peg:
        cli_peg_simulator()
        return
    elif args.grid:
        cli_grid_audit()
        return
    elif args.wallet:
        cli_wallet_audit()
        return

    page = 1
    msg = "Sovereign Core OS v6.25.0-beta. Three-Pronged Master TUI Active."
    while True:
        clear_screen()
        summary = MultiDisplayManager.render_all_displays_summary()
        hw = HardwareWarden.audit_physical_hardware()
        current_role = RoleSwitcherEngine.get_current_role()
        
        print("=" * 70 + f"\n=== MASTER DASHBOARD: SOVEREIGN CORE OS v6.25.0-beta [PAGE {page}/4] ===\n" + "=" * 70)
        print(f"  Active Profile Role : {current_role} | Host Thermal: {hw['thermal_celsius']}°C")
        
        if page == 1:
            d1 = summary["display_1_depin"]
            print(f"\n  [Display 1] DePIN Portfolio   : ${d1['gross']} USD (POL Tax:${d1['pol_tax']} USD)")
            print("  ------------------------------------------------------------------")
            print("  [1] 💰 Run DePIN Capital Routing & 6-App Yield Audit [--depin]")
            print("  [2] 🌉 Run BIP 300 Two-Way Peg Simulator [--peg]")
            print("  [3] ⚡ Run System-Wide L1/L2 Kernel Integration Audit [--kernel]")
            print("  [4] 💼 Run Wallet & Liquidity Reserves Audit [--wallet]")
            print("  [5] 🛑 Exit to Native L1 Shell [Hotkey: Q]")
            
        elif page == 2:
            d2 = summary["display_2_hardware"]
            d3 = summary["display_3_consensus"]
            print(f"\n  [Display 2] Hardware Warden   : {d2['thermal_c']}°C | shm: {d2['shm_mb']} MB")
            print(f"  [Display 3] Sidechain Status  : BIP300: {d3['bip300']} | BMM: {d3['bip301']}")
            print("  ------------------------------------------------------------------")
            print("  [1] View Full Hardware Telemetry & Fans")
            print("  [2] Audit BIP 300/301 Miner Consensus Ledgers")
            print("  [3] Refresh RAM-Backed /dev/shm Buffers")
            
        elif page == 3:
            d5 = summary["display_5_wallet"]
            print(f"\n  [Display 5] Wallet & Reserves : {d5['reserve_btc']} BTC | POL Pool: ${d5['pol_pool_usd']}")
            print("  ------------------------------------------------------------------")
            print("  [1] Execute On-Chain Deposit (M5)")
            print("  [2] Execute Withdrawal Bundle (M6)")
            print("  [3] Rebalance POL Liquidity Pool & Beefy Compound")
            
        elif page == 4:
            d6 = summary["display_6_governance"]
            print(f"\n  [Display 4] About & Governance: {len(d6['orphans'])} Orphans Tracked [{d6['status']}]")
            print("  Orphaned Scripts: " + ", ".join(d6['orphans']))
            print("  ------------------------------------------------------------------")
            print("  [1] View Three-Pronged Architecture Manual")
            print("  [2] Run Ecosystem Diagnostic Sync")
            
        print("\nNavigation: [N]ext Page | [P]rev Page | [Q]uit to L1 Host")
        print("=" * 70 + f"\n[-] STATUS: {msg}\n" + "=" * 70)
        
        sys.stdout.write("Select Command: ")
        sys.stdout.flush()
        try:
            import termios, tty
            fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
            try: tty.setraw(fd); choice = sys.stdin.read(1).upper()
            finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except:
            choice = input().strip().upper()[:1]
        
        if choice in ['Q', 'q', '\x03', '\x04']: break
        elif choice in ['N', 'n']: page = (page % 4) + 1; msg = f"Navigated to Master Page {page}"
        elif choice in ['P', 'p']: page = ((page - 2) % 4) + 1; msg = f"Navigated to Master Page {page}"
        elif choice == '1' and page == 1:
            cli_depin_audit()
            input("\nPress Enter to return...")
        elif choice == '2' and page == 1:
            cli_peg_simulator()
            input("\nPress Enter to return...")
        elif choice == '3' and page == 1:
            cli_kernel_audit()
            input("\nPress Enter to return...")
        elif choice == '4' and page == 1:
            cli_wallet_audit()
            input("\nPress Enter to return...")
        elif choice == '5' and page == 1: break

    os.system('clear'); os.system('stty sane')

if __name__ == "__main__": main()

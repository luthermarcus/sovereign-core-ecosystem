import sqlite3, os, time

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sovereign_metrics.db")

def run_amm_swap():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    print("   Sovereign Core v1.20.0-beta [EIP-4337 AMM & TAX WAIVER ENGINE]")
    print("=" * 80)
    
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    
    try:
        token_in = input("\n[?] Enter Token to Sell (e.g., FOX, BTC): ").strip().upper()
        c.execute("SELECT balance, price_usd FROM global_assets_v7 WHERE token=?", (token_in,))
        res_in = c.fetchone()
        if not res_in or res_in[0] <= 0:
            print(f"\n[!] Error: Insufficient balance."); time.sleep(2); return
            
        balance_in, price_in = res_in
        print(f"    Available Balance: {balance_in:,.4f} {token_in}")
        amount_in = float(input(f"[?] Enter amount to swap: ").strip())
        
        token_out = input("[?] Enter Token to Buy (e.g., USDC, SOL): ").strip().upper()
        c.execute("SELECT balance, price_usd FROM global_assets_v7 WHERE token=?", (token_out,))
        res_out = c.fetchone()
        balance_out, price_out = res_out if res_out else (0.0, price_in)

        # Developer Sandbox Bypass Check
        c.execute("SELECT setting_value FROM user_settings_v14 WHERE setting_key='sandbox_bypass'")
        sandbox_flag = c.fetchone()
        sandbox_mode = sandbox_flag and sandbox_flag[0] == 'ENABLED'
        
        eco_tax = 0.0 if sandbox_mode else amount_in * 0.05
        
        if sandbox_mode:
            print(f"    [+] Sandbox Mode: minrelaytxfee equivalent set to 0.")
        else:
            print(f"    [+] Ethical Protocol Tax: 5% captured for Ecosystem Treasury ({eco_tax:.4f} {token_in}).")

        swap_amount = amount_in - eco_tax
        amount_out = ((2500000.0/2/price_out) * (swap_amount * 0.997)) / ((2500000.0/2/price_in) + (swap_amount * 0.997))
        
        print(f"\n[Route] UserOperation -> AMM Pool | [Output] {amount_out:.6f} {token_out} delivered.")
        
        if input("\n[?] Execute cross-chain transaction? (y/N): ").strip().lower() == 'y':
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (balance_in - amount_in, token_in))
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (balance_out + amount_out, token_out))
            conn.commit()
            print("\n[+] Trade Executed. Balances atomically updated via WAL.")
        else:
            print("\n[-] Cancelled.")
    except Exception as e:
        print(f"\n[!] Trade Error: {str(e)}")
    finally:
        conn.close()
        time.sleep(2)

if __name__ == "__main__":
    run_amm_swap()

import sqlite3, os, time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_amm_swap():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    print("   Sovereign Core v1.11.0-beta [EIP-4337 AMM & TAX WAIVER ENGINE]")
    print("=" * 80)
    
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    
    try:
        token_in = input("\n[?] Enter Token to Sell (e.g., FOX, BTC, USDC): ").strip().upper()
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

        # ZERO-FEE SANDBOX BYPASS
        print("\n--- ⚙️ Developer Tax Policies ---")
        sandbox_mode = input("[?] Apply Developer Sandbox Zero-Fee Bypass? (y/N): ").strip().lower() == 'y'
        
        if sandbox_mode:
            eco_tax = 0.0
            print(f"    [+] Sandbox Mode Active: minrelaytxfee equivalent set to 0. Tax completely waived.")
        else:
            eco_tax = amount_in * 0.05
            print(f"    [+] Ethical Protocol Tax: 5% captured for Ecosystem Treasury ({eco_tax:.4f} {token_in}).")

        swap_amount = amount_in - eco_tax
        
        pool_symbol = f"{token_in}/{token_out}"
        c.execute("SELECT liquidity_usd FROM liquidity_pairs WHERE pair_symbol=?", (pool_symbol,))
        liq_res = c.fetchone()
        liquidity_usd = liq_res[0] if liq_res else 1000000.0 
        
        reserve_in = (liquidity_usd / 2) / price_in
        reserve_out = (liquidity_usd / 2) / price_out
        amount_out = (reserve_out * (swap_amount * 0.997)) / (reserve_in + (swap_amount * 0.997))
        
        print("\n--- 💱 Execution ---")
        print(f" [Route] UserOperation -> AMM Pool (${liquidity_usd:,.2f} Liq)")
        print(f" [Output] {amount_out:.6f} {token_out} received to wallet.")
        
        confirm = input("\n[?] Execute cross-chain transaction? (y/N): ").strip().lower()
        if confirm == 'y':
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (balance_in - amount_in, token_in))
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (balance_out + amount_out, token_out))
            
            if not sandbox_mode:
                pol_cut = eco_tax * 0.40
                burn_cut = eco_tax * 0.40
                insurance_cut = eco_tax * 0.20
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                c.execute("INSERT OR IGNORE INTO protocol_treasury_v11 (asset, pol_locked, total_burned, insurance_fund, last_updated) VALUES (?, 0, 0, 0, ?)", (token_in, timestamp))
                c.execute("UPDATE protocol_treasury_v11 SET pol_locked=pol_locked+?, total_burned=total_burned+?, insurance_fund=insurance_fund+?, last_updated=? WHERE asset=?", (pol_cut, burn_cut, insurance_cut, timestamp, token_in))
            
            conn.commit()
            print("\n[+] Trade Executed. Balances and tax policies atomically updated via WAL.")
        else:
            print("\n[-] Swap cancelled.")
    except Exception as e:
        print(f"\n[!] Trade Error: {str(e)}")
    finally:
        conn.close()
        time.sleep(4)

if __name__ == "__main__":
    run_amm_swap()

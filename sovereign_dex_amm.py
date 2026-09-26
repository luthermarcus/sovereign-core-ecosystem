import sqlite3, os, time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_amm_swap():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    print("   Sovereign Core v1.12.0-beta [AMM & DEVELOPER ROYALTY ROUTER]")
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

        # Developer Sandbox Bypass Prompt
        sandbox_mode = input("\n[?] Apply Developer Sandbox Zero-Fee Bypass? (y/N): ").strip().lower() == 'y'
        
        if sandbox_mode:
            eco_tax = 0.0
            print("    [+] Sandbox Mode: Zero-Fee bypass active. No taxes deducted.")
        else:
            eco_tax = amount_in * 0.05
            dev_cut = eco_tax * 0.20 # 1% of total (5% of tax) to App Devs
            pol_cut = eco_tax * 0.40 # 2% to POL
            burn_cut = eco_tax * 0.20 # 1% Burn
            guard_cut = eco_tax * 0.20 # 1% Insurance
            print(f"    [+] 5% Fee Intercepted: POL={pol_cut:.4f} | Devs={dev_cut:.4f} | Guard={guard_cut:.4f} | Burn={burn_cut:.4f}")

        swap_amount = amount_in - eco_tax
        pool_symbol = f"{token_in}/{token_out}"
        c.execute("SELECT liquidity_usd FROM liquidity_pairs WHERE pair_symbol=?", (pool_symbol,))
        liq_res = c.fetchone()
        liquidity_usd = liq_res[0] if liq_res else 1000000.0 
        
        reserve_in = (liquidity_usd / 2) / price_in
        reserve_out = (liquidity_usd / 2) / price_out
        amount_out = (reserve_out * (swap_amount * 0.997)) / (reserve_in + (swap_amount * 0.997))
        
        print(f"\n[Route] EIP-4337 UserOp -> AMM (${liquidity_usd:,.2f} Pool)")
        print(f"[Output] {amount_out:.6f} {token_out} delivered.")
        
        confirm = input("\n[?] Confirm Trade? (y/N): ").strip().lower()
        if confirm == 'y':
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (balance_in - amount_in, token_in))
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (balance_out + amount_out, token_out))
            if not sandbox_mode:
                c.execute("UPDATE dev_registry_v13 SET total_earned = total_earned + ? WHERE dev_id='DEV-01'", (dev_cut,))
            conn.commit()
            print("\n[+] Trade confirmed and balances updated atomically.")
        else:
            print("\n[-] Cancelled.")
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
    finally:
        conn.close()
        time.sleep(3)

if __name__ == "__main__":
    run_amm_swap()

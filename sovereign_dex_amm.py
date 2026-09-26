import sqlite3, os, time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def run_amm_swap():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    print("   Sovereign Core v1.7.0-beta [EIP-4337 AMM SWAP ENGINE]")
    print("=" * 80)
    
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    
    try:
        token_in = input("\n[?] Enter Token to Sell (e.g., FOX, BTC, USDC): ").strip().upper()
        token_out = input("[?] Enter Token to Buy (e.g., USDC, SOL, ETH): ").strip().upper()

        # RISK GUARDIAN EMERGENCY FREEZE CHECK
        c.execute("SELECT reason FROM risk_guardian_freezes WHERE asset=? OR asset=?", (token_in, token_out))
        freeze_res = c.fetchone()
        if freeze_res:
            print(f"\n[!] 🚨 EMERGENCY GUARDIAN ACTIVE: Trading for {token_in}/{token_out} is frozen.")
            print(f"    Reason: {freeze_res[0]}")
            print(f"    Status: Withdrawals-Only mode enabled. AMM Swaps blocked to protect users.")
            time.sleep(5)
            return

        c.execute("SELECT balance, price_usd FROM global_assets_v7 WHERE token=?", (token_in,))
        res_in = c.fetchone()
        if not res_in or res_in[0] <= 0:
            print(f"\n[!] Error: Insufficient {token_in} balance or asset not tracked.")
            time.sleep(2)
            return
            
        balance_in, price_in = res_in
        print(f"    Available {token_in} Balance: {balance_in:,.4f}")
        
        amount_in = float(input(f"[?] Enter amount of {token_in} to swap: ").strip())
        if amount_in > balance_in:
            print(f"\n[!] Error: Amount exceeds available balance.")
            time.sleep(2)
            return
            
        c.execute("SELECT balance, price_usd FROM global_assets_v7 WHERE token=?", (token_out,))
        res_out = c.fetchone()
        balance_out, price_out = res_out if res_out else (0.0, price_in) # Fallback handling
        
        pool_symbol = f"{token_in}/{token_out}"
        alt_pool = f"{token_out}/{token_in}"
        c.execute("SELECT liquidity_usd FROM liquidity_pairs WHERE pair_symbol=? OR pair_symbol=?", (pool_symbol, alt_pool))
        liq_res = c.fetchone()
        
        liquidity_usd = liq_res[0] if liq_res else 1000000.0 
        reserve_in = (liquidity_usd / 2) / price_in
        reserve_out = (liquidity_usd / 2) / price_out
        
        amount_in_with_fee = amount_in * 0.997
        amount_out = (reserve_out * amount_in_with_fee) / (reserve_in + amount_in_with_fee)
        expected_out = (amount_in * price_in) / price_out
        slippage = ((expected_out - amount_out) / expected_out) * 100 if expected_out > 0 else 0
        
        print("\n--- 💱 Execution Simulation ---")
        print(f" [Route] UserOperation Bundler -> AMM Pool (${liquidity_usd:,.2f} Liq)")
        print(f" [Paymaster] Gas abstracted via 0.3% LP Swap Fee.")
        print(f" [Output] {amount_out:.6f} {token_out}")
        print(f" [Slippage] {slippage:.2f}% Price Impact")
        
        confirm = input("\n[?] Confirm and execute swap? (y/N): ").strip().lower()
        if confirm == 'y':
            new_bal_in = balance_in - amount_in
            new_bal_out = balance_out + amount_out
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (new_bal_in, token_in))
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (new_bal_out, token_out))
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("INSERT OR REPLACE INTO scraper_flags (flag_id, status, description, detected_at) VALUES (?, ?, ?, ?)", (f'FLAG_DEX_SWAP', 'GREEN', f'Swap {amount_in} {token_in} -> {token_out} completed.', timestamp))
            conn.commit()
            print("\n[+] EIP-4337 Trade Executed. Balances atomically updated.")
        else:
            print("\n[-] Swap cancelled.")
            
    except Exception as e:
        print(f"\n[!] Trade Execution Error: {str(e)}")
    finally:
        conn.close()
        time.sleep(3)

if __name__ == "__main__":
    run_amm_swap()

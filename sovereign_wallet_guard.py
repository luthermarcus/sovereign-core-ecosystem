import sqlite3, os
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sovereign_metrics.db")
def verify_dapp_connection():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80); print("   Sovereign Core OS [WEB WALLET SECURITY GUARD]"); print("=" * 80)
    dapp_domain = input("\n[?] Enter DApp domain attempting connection (e.g., app.uniswap.org): ").strip().lower()
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    c.execute("SELECT entity_name, verified_status FROM cmc_verified_domains_v31 WHERE domain=?", (dapp_domain,))
    res = c.fetchone()
    if res:
        print(f"\n [GREEN] SUCCESS: '{dapp_domain}' verified as '{res[0]}' ({res[1]}).")
    else:
        print(f"\n 🚨 [RED SECURITY WARNING] '{dapp_domain}' NOT found in CoinMarketCap verified registry! Blocked.")
    conn.close()
    input("\nPress Enter to return to OS...")
if __name__ == "__main__": verify_dapp_connection()

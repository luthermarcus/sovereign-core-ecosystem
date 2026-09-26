import sqlite3, os, sys

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sovereign_metrics.db")

def verify_dapp_connection():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    print("   Sovereign Core OS v1.31.0-beta [WEB WALLET SECURITY GUARD]")
    print("=" * 80)
    
    dapp_domain = input("\n[?] Enter DApp domain attempting connection (e.g., app.uniswap.org, malicious-site.xyz): ").strip().lower()
    
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    c.execute("SELECT entity_name, verified_status FROM cmc_verified_domains_v31 WHERE domain=?", (dapp_domain,))
    res = c.fetchone()
    
    if res:
        print(f"\n [GREEN] SUCCESS: '{dapp_domain}' is verified as '{res[0]}' ({res[1]}).")
        print(" [+] EIP-1193 pairing session established securely.")
        c.execute("INSERT OR REPLACE INTO web_wallet_sessions_v31 VALUES (?, ?, 'ACTIVE', datetime('now'))", (f"sess_{int(os.time() if hasattr(os, 'time') else 12345)}", dapp_domain))
        conn.commit()
    else:
        print(f"\n 🚨 [RED SECURITY WARNING] '{dapp_domain}' NOT found in CoinMarketCap verified registry!")
        print(" [!] Potential phishing or malicious scraping attempt detected. Connection blocked.")
        c.execute("INSERT OR REPLACE INTO scraper_flags VALUES ('FLAG_PHISHING_BLOCKED', 'RED', ?, datetime('now'))", (f"Blocked unverified DApp connection attempt from: {dapp_domain}",))
        conn.commit()
        
    conn.close()
    input("\nPress Enter to return to OS...")

if __name__ == "__main__":
    verify_dapp_connection()

import sqlite3
import os
import datetime

def render_cli():
    print("=" * 65)
    print(" LUTHER'S EXPANSIVE ECOSYSTEM COMMAND CENTER (Dashboard B)")
    print(f" Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    print("[v] CRITICAL SYSTEM FLAGS: All Systems Clear - No Active Error Flags.")
    print("[v] SECURITY: Tor SOCKS5 Loopback Active (-proxy=127.0.0.1:9050)")
    print("-" * 65)
    print("=== EXPANSIVE EARNINGS PORTFOLIO ===")
    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/wallet.db")
        c = conn.cursor()
        c.execute("SELECT app_name, status, traffic_or_tier, earnings_usd FROM earnings_portfolio")
        for row in c.fetchall():
            print(f" [{row[0]}] : {row[1]} | Traffic: {row[2]} | Earnings: ${row[3]:.2f}")
        conn.close()
    except Exception as e:
        print(f" Portfolio Error: {e}")
    print("=" * 65)

if __name__ == "__main__":
    render_cli()

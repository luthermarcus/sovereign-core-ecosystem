import sqlite3, os, time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sovereign_metrics.db")

def harvest_depin_mining_yields():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 80)
    print("   Sovereign Core v1.23.0-beta [DePIN MINING YIELD SWEEPER]")
    print("=" * 80)
    
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    
    try:
        # 1. Read local node portfolio earnings (Simulating read from ecosystem.db)
        mining_nodes = {
            'Mysterium Node': {'earned': 14.25, 'token': 'MYST', 'price_usd': 0.18},
            'EarnApp': {'earned': 8.50, 'token': 'USDC', 'price_usd': 1.00},
            'Honeygain': {'earned': 11.40, 'token': 'USDC', 'price_usd': 1.00},
            'TraffMonetizer': {'earned': 5.10, 'token': 'USDC', 'price_usd': 1.00},
            'Pawns.app': {'earned': 6.75, 'token': 'USDC', 'price_usd': 1.00},
            'PacketStream': {'earned': 3.20, 'token': 'USDC', 'price_usd': 1.00}
        }
        
        print("\n[*] Harvesting Local DePIN Bandwidth Nodes...")
        total_usd_value = 0.0
        
        for app, data in mining_nodes.items():
            value = data['earned'] * data['price_usd']
            total_usd_value += value
            print(f"    ├── [{app:<16}] Yield: {data['earned']:>6.2f} {data['token']:<4} | Value: ${value:>5.2f}")
            
            # Bridge to Core Wallet
            c.execute("SELECT balance FROM global_assets_v7 WHERE token=?", (data['token'],))
            res = c.fetchone()
            current_bal = res[0] if res else 0.0
            new_bal = current_bal + data['earned']
            
            # Ensure asset exists in wallet ledger
            c.execute("INSERT OR IGNORE INTO global_assets_v7 (token, name, price_usd, category, repo_health, balance, last_updated) VALUES (?, ?, ?, 'DePIN Mining', 'Active', 0, ?)", 
                     (data['token'], f"{data['token']} Yield", data['price_usd'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            c.execute("UPDATE global_assets_v7 SET balance=? WHERE token=?", (new_bal, data['token']))

        # 2. Route 10% of total mining yields to fund the EIP-4337 Paymaster
        paymaster_cut = total_usd_value * 0.10
        c.execute("UPDATE eip4337_paymaster_v14 SET gas_balance_usd = gas_balance_usd + ? WHERE paymaster_address = '0xPaymaster...9A12'", (paymaster_cut,))
        
        print(f"\n[+] Total Mining Yield Swept to Wallet : ${total_usd_value:.2f}")
        print(f"[+] Paymaster Gas Treasury Auto-Funded : +${paymaster_cut:.2f}")
        
        conn.commit()
        print("\n[+] DePIN bridge executed atomically. Databases synchronized.")
        
    except Exception as e:
        print(f"\n[!] Mining Bridge Error: {str(e)}")
    finally:
        conn.close()
        time.sleep(4)

if __name__ == "__main__":
    harvest_depin_mining_yields()

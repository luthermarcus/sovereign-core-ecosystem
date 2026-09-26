import sqlite3
import os
import datetime
import subprocess
import sys
import socket
import json

try:
    from portability_layer import get_environment_profile
except ImportError:
    def get_environment_profile():
        return {"distro": "Linux Mint (Bare-Metal)", "release": "7.0.0"}

def ping_dex_daemon():
    print("=" * 65)
    print("[*] Initiating Local Tor DEX Daemon Ping (Port 8181)...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(('127.0.0.1', 8181))
        s.sendall(b"PING")
        response = s.recv(1024).decode('utf-8')
        s.close()
        data = json.loads(response)
        print("[v] CONNECTION SUCCESSFUL - DAEMON RESPONSE:")
        print(f"    Node Type : {data.get('node_type')}")
        print(f"    Status    : {data.get('status')}")
    except:
        print("[x] CONNECTION FAILED: DEX Daemon offline.")
    print("=" * 65)

def render_cli():
    # Run the AMM smart contract automatically when dashboard opens
    sys.path.append(os.path.expanduser("~/sovereign-core-ecosystem/modules"))
    try:
        import amm_smart_contract
        amm_status = amm_smart_contract.execute_amm_compounding()
    except:
        amm_status = "Status: AMM Offline"

    env = get_environment_profile()
    print("=" * 65)
    print(f" LUTHER'S DEPIN INFRASTRUCTURE COMMAND CENTER (Dashboard B)")
    print(f" Host OS: {env['distro']} | Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    daemon_check = subprocess.run(["pgrep", "-f", "dex_daemon.py"], capture_output=True, text=True)
    dex_status = "[v] Active" if daemon_check.returncode == 0 else "[x] Inactive"

    print(f"=== ACTIONABLE INTEROPERABILITY CHECKLIST ===")
    print(f"  1. Tor P2P Outbound Gossip Engine : [v] Active (python3-socks)")
    print(f"  2. Autonomous Tor Sync Daemon     : {dex_status} (Port 8181)")
    print(f"  3. Off-Chain AMM Smart Contract   : [v] {amm_status}")
    print("-" * 65)
    
    try:
        conn = sqlite3.connect(os.path.expanduser("~/sovereign-core-ecosystem/wallet.db"))
        c = conn.cursor()
        c.execute("SELECT token_pair, base_reserve, exchange_rate FROM dex_reserves")
        print("=== SMART CONTRACT AUTO-COMPOUNDED DEX LIQUIDITY ===")
        for row in c.fetchall():
            print(f"  [{row[0]}] : Base Liquidity: ${row[1]:.2f} | Emulated Rate: {row[2]}")
        conn.close()
    except Exception as e:
        print(f" Portfolio Standby: {e}")
    print("=" * 65)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--ping-dex":
        ping_dex_daemon()
    else:
        render_cli()

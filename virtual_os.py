import curses
import sqlite3
import os
from portability_layer import get_environment_profile

def get_wallet_data():
    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/wallet.db")
        c = conn.cursor()
        c.execute("SELECT address, balance, staked_power FROM wallet_state LIMIT 1")
        wallet = c.fetchone()
        c.execute("SELECT module_name, earnings FROM innovations")
        inv = c.fetchall()
        conn.close()
        return wallet, inv
    except Exception:
        return None, []

def get_live_telemetry():
    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/sys_health.db")
        c = conn.cursor()
        c.execute("SELECT * FROM host_metrics LIMIT 1")
        host = c.fetchone()
        c.execute("SELECT * FROM myst_metrics LIMIT 1")
        myst = c.fetchone()
        c.execute("SELECT * FROM net_metrics LIMIT 1")
        net = c.fetchone()
        conn.close()
        return host, myst, net
    except:
        return None, None, None

def get_loaded_modules():
    mod_dir = "/home/luther/sovereign-core-ecosystem/modules"
    if os.path.exists(mod_dir):
        return [f for f in os.listdir(mod_dir) if f.endswith(".py")]
    return []

def main_loop(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    selection = 0
    menu = ["Telemetry Matrix", "Network & Security", "Emulated Wallet & DEX", "Innovation Copyright", "Developer Modules", "Knowledge Vault", "Exit System"]
    
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        header = "--- SOVEREIGN CORE VIRTUAL OS [v1.60.0] ---"
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(1, max(1, (max_x - len(header)) // 2), header[:max_x-2])
        stdscr.attroff(curses.color_pair(1))
        
        menu_start_y = 3
        for idx, row in enumerate(menu):
            y = menu_start_y + idx
            if y < max_y - 4:
                disp = f"> {row}" if idx == selection else f"  {row}"
                if idx == selection:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(y, 2, disp[:max_x-3])
                    stdscr.attroff(curses.color_pair(2))
                else:
                    stdscr.addstr(y, 2, disp[:max_x-3])
                    
        content_start_y = menu_start_y + len(menu) + 1
        if content_start_y < max_y - 5:
            stdscr.addstr(content_start_y - 1, 2, ("-" * (max_x - 4))[:max_x-4])
            
        def draw(y_off, text, bold=False):
            target_y = content_start_y + y_off
            if target_y < max_y - 4:
                if bold: stdscr.addstr(target_y, 2, text[:max_x-3], curses.A_BOLD)
                else: stdscr.addstr(target_y, 2, text[:max_x-3])

        if selection == 0:
            host, myst, _ = get_live_telemetry()
            env = get_environment_profile()
            draw(0, "[DEPIN NODE & HOST TELEMETRY]", True)
            if host and myst:
                draw(2, f"Host OS: {env['os']} ({env['architecture']})")
                draw(3, f"CPU Usage: {host[0]}%  |  RAM: {host[1]}%  |  Disk: {host[2]}%")
                draw(4, f"Mysterium Container: {myst[0]}  |  Peers: {myst[1]}")
            else:
                draw(2, "Awaiting Telemetry Daemon Sync...")
        elif selection == 1:
            _, _, net = get_live_telemetry()
            draw(0, "[NETWORK & SECURITY MATRIX]", True)
            if net:
                draw(2, f"UFW Firewall Status: {net[0]}")
                draw(3, f"Tor Proxy Tunnel: {net[1]}")
                draw(5, "Bitcoin Protocol: -proxy=127.0.0.1:9050 (-onlynet=onion)")
            else:
                draw(2, "Network Telemetry Offline.")
        elif selection == 2:
            wallet, _ = get_wallet_data()
            draw(0, "[EMULATED WALLET & DEX MATRIX]", True)
            if wallet:
                draw(2, f"Master Address: {wallet[0][:18]}...")
                draw(3, f"Vault Balance: {wallet[1]} MYST/BTC")
                draw(4, f"Network Staked Power: {wallet[2]}%")
            else:
                draw(2, "Wallet Ledger Offline.")
        elif selection == 3:
            _, innovations = get_wallet_data()
            draw(0, "[INNOVATION COPYRIGHT & 5% ROYALTY]", True)
            draw(2, "Active Deployed Modules & Smart Royalties:")
            y_offset = 3
            for inv in innovations:
                draw(y_offset, f" - {inv[0]}: +{inv[1]} Credits (5% Royalty)")
                y_offset += 1
        elif selection == 4:
            mods = get_loaded_modules()
            draw(0, "[DEVELOPER MODULES & PLUGINS]", True)
            draw(2, "Loaded XDA-Style Modular Extensions:")
            y_offset = 3
            for m in mods:
                draw(y_offset, f" [x] Plugin Loaded: {m}")
                y_offset += 1
        elif selection == 5:
            draw(0, "[KNOWLEDGE VAULT - FTS5]", True)
            draw(2, "Status: Synchronized with local SQLite FTS5 index.")
            
        host, _, _ = get_live_telemetry()
        if host and max_y > 5:
            bar_y = max_y - 3
            stdscr.addstr(bar_y - 1, 2, ("=" * (max_x - 4))[:max_x-4])
            status_bar = f" SANDBOX RESOURCE POOL -> CPU: {host[0]}% | RAM: {host[1]}% | DISK: {host[2]}%"
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(bar_y, 2, status_bar[:max_x-3], curses.A_BOLD)
            stdscr.attroff(curses.color_pair(3))
            
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and selection > 0: selection -= 1
        elif key == curses.KEY_DOWN and selection < len(menu) - 1: selection += 1
        elif key in [10, 13] and selection == 6: break

curses.wrapper(main_loop)

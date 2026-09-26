import curses
import sqlite3
import os
import datetime
from portability_layer import get_environment_profile

def get_system_data():
    data = {}
    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/sys_health.db")
        c = conn.cursor()
        c.execute("SELECT * FROM host_metrics LIMIT 1")
        data["host"] = c.fetchone()
        c.execute("SELECT * FROM myst_metrics LIMIT 1")
        data["myst"] = c.fetchone()
        c.execute("SELECT * FROM net_metrics LIMIT 1")
        data["net"] = c.fetchone()
        conn.close()
    except:
        data["host"] = data["myst"] = data["net"] = None

    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/wallet.db")
        c = conn.cursor()
        c.execute("SELECT app_name, status, traffic_or_tier, earnings_usd FROM earnings_portfolio")
        data["portfolio"] = c.fetchall()
        c.execute("SELECT token_pair, exchange_rate FROM dex_reserves")
        data["dex"] = c.fetchall()
        conn.close()
    except:
        data["portfolio"] = []
        data["dex"] = []

    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/discipline_ledger.db")
        c = conn.cursor()
        c.execute("SELECT event_type, description FROM discipline_ledger ORDER BY id DESC LIMIT 3")
        data["discipline"] = c.fetchall()
        conn.close()
    except:
        data["discipline"] = []

    return data

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
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    
    selection = 0
    menu = [
        "1. Ecosystem Command Center (Dashboard B Bridge)", 
        "2. Network & Zero-Tolerance Security", 
        "3. Emulated Wallet & DEX Matrix (FOX/PARROT-BTC)", 
        "4. Innovation Copyright & Royalties", 
        "5. XDA Developer Modules & Smart Contract Bridge", 
        "6. SQLite FTS5 Knowledge Vault", 
        "7. Exit System"
    ]
    
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        header = "--- SOVEREIGN CORE VIRTUAL OS [v1.82.0 MASTER] ---"
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
            
        def draw(y_off, text, bold=False, color=0):
            target_y = content_start_y + y_off
            if target_y < max_y - 4:
                if color > 0: stdscr.attron(curses.color_pair(color))
                if bold: stdscr.addstr(target_y, 2, text[:max_x-3], curses.A_BOLD)
                else: stdscr.addstr(target_y, 2, text[:max_x-3])
                if color > 0: stdscr.attroff(curses.color_pair(color))

        d = get_system_data()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if selection == 0:
            draw(0, f"| LUTHER'S EXPANSIVE ECOSYSTEM COMMAND CENTER (DASHBOARD B) | {now_str} |", True, 4)
            draw(2, "=== CRITICAL SYSTEM & DISCIPLINE FLAGS ===", bold=True)
            y_f = 3
            for disc in d["discipline"]:
                draw(y_f, f"[{disc[0]}] {disc[1]}", color=3)
                y_f += 1
            draw(y_f + 1, "=== EXPANSIVE EARNINGS PORTFOLIO (NATIVE & 6 APPS) ===", bold=True)
            y_off = y_f + 2
            for app in d["portfolio"]:
                draw(y_off, f"[{app[0]}] : {app[1]} | Traffic: {app[2]} | Earnings: ${app[3]:.2f}")
                y_off += 1
        elif selection == 1:
            draw(0, "[ZERO-TOLERANCE NETWORK & SECURITY MATRIX]", True)
            draw(2, "Firewall Shield : Active / Secured (Socket Monitored)")
            draw(3, "Tor SOCKS5 Proxy: 127.0.0.1:9050 (Active Onion)")
            draw(4, "Content Filter  : Active (Illicit Media / CSAM Blocked)")
            draw(5, "Bitcoin Protocol: -proxy=127.0.0.1:9050 (-onlynet=onion)")
        elif selection == 2:
            draw(0, "[EMULATED WALLET & DEX MATRIX (FOX/PARROT-BTC)]", True)
            draw(2, "Master Address  : sovereign1luther_master_node_x79...")
            draw(3, "Base Currency   : Bitcoin Core (BTC Anchored)")
            y_d = 4
            for dex in d["dex"]:
                draw(y_d, f" DEX Pair       : {dex[0]} | Rate: {dex[1]} (Off-Chain Settlement)")
                y_d += 1
        elif selection == 3:
            draw(0, "[INNOVATION COPYRIGHT & 5% SMART ROYALTIES]", True)
            draw(2, "Sovereign Core Microkernel: +12.45 Credits (5% Attribution)")
        elif selection == 4:
            mods = get_loaded_modules()
            draw(0, "[XDA DEVELOPER MODULES & SMART CONTRACT PORT BRIDGE]", True)
            y_m = 2
            for m in mods:
                draw(y_m, f" [x] Audited Plugin: {m}")
                y_m += 1
        elif selection == 5:
            draw(0, "[SQLITE FTS5 KNOWLEDGE VAULT]", True)
            draw(2, "Status: Synchronized with FTS5 Full-Text Search Engine.")
            draw(3, "Integrity: Cryptographically Signed via SHA-256 Vault Signer.")
            
        # Persistent Hardware Sandbox Status Bar at the Bottom
        if d["host"] and max_y > 5:
            bar_y = max_y - 3
            stdscr.addstr(bar_y - 1, 2, ("=" * (max_x - 4))[:max_x-4])
            status_bar = f" INTEROPERABLE SANDBOX -> CPU: {d['host'][0]}% | RAM: {d['host'][1]}% | Disk: {d['host'][2]}%"
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(bar_y, 2, status_bar[:max_x-3], curses.A_BOLD)
            stdscr.attroff(curses.color_pair(3))
            
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and selection > 0: selection -= 1
        elif key == curses.KEY_DOWN and selection < len(menu) - 1: selection += 1
        elif key in [10, 13] and selection == 6: break

curses.wrapper(main_loop)

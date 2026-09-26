import curses
import sqlite3

def get_wallet_data():
    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/wallet.db")
        c = conn.cursor()
        c.execute("SELECT address, balance, staked_power FROM wallet_state LIMIT 1")
        wallet = c.fetchone()
        c.execute("SUM(earnings) FROM innovations") # or fetch rows
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
        conn.close()
        return host, myst
    except:
        return None, None

def main_loop(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selection = 0
    menu = ["Telemetry Matrix", "Emulated Wallet & DEX", "Innovation Copyright", "Knowledge Vault", "Exit System"]
    
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        header = "--- SOVEREIGN CORE VIRTUAL OS [v1.54.0] ---"
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(1, max(1, (max_x - len(header)) // 2), header[:max_x-2])
        stdscr.attroff(curses.color_pair(1))
        
        menu_start_y = 3
        for idx, row in enumerate(menu):
            y = menu_start_y + idx
            if y < max_y - 1:
                disp = f"> {row}" if idx == selection else f"  {row}"
                if idx == selection:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(y, 2, disp[:max_x-3])
                    stdscr.attroff(curses.color_pair(2))
                else:
                    stdscr.addstr(y, 2, disp[:max_x-3])
                    
        content_start_y = menu_start_y + len(menu) + 2
        if content_start_y < max_y - 2:
            stdscr.addstr(content_start_y - 1, 2, ("-" * (max_x - 4))[:max_x-4])
            
        def draw(y_off, text, bold=False):
            if content_start_y + y_off < max_y - 1:
                if bold: stdscr.addstr(content_start_y + y_off, 2, text[:max_x-3], curses.A_BOLD)
                else: stdscr.addstr(content_start_y + y_off, 2, text[:max_x-3])

        if selection == 0:
            host, myst = get_live_telemetry()
            draw(0, "[DEPIN NODE & HARDWARE TELEMETRY]", True)
            if host and myst:
                draw(2, f"CPU: {host[0]}%  |  RAM: {host[1]}%  |  DISK: {host[2]}%")
                draw(4, f"Mysterium Node: {myst[0]}  |  Connections: {myst[1]}")
            else:
                draw(2, "Awaiting Telemetry Daemon Sync...")
        elif selection == 1:
            wallet, _ = get_wallet_data()
            draw(0, "[EMULATED WALLET & DEX MATRIX]", True)
            if wallet:
                draw(2, f"Master Address: {wallet[0][:20]}...")
                draw(3, f"Balance: {wallet[1]} MYST/BTC  |  Staked Power: {wallet[2]}%")
                draw(5, "Bitcoin Protocol: Tor-Only (-proxy=127.0.0.1:9050)")
            else:
                draw(2, "Wallet Ledger Offline.")
        elif selection == 2:
            _, innovations = get_wallet_data()
            draw(0, "[INNOVATION COPYRIGHT & 5% ROYALTY]", True)
            draw(2, "Active Deployed Modules & Smart Royalties:")
            y_offset = 3
            for inv in innovations:
                draw(y_offset, f" - {inv[0]}: +{inv[1]} Credits (5% Royalty)")
                y_offset += 1
        elif selection == 3:
            draw(0, "[KNOWLEDGE VAULT - FTS5]", True)
            draw(2, "Status: Synchronized with local SQLite FTS5 index.")
            
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and selection > 0: selection -= 1
        elif key == curses.KEY_DOWN and selection < len(menu) - 1: selection += 1
        elif key in [10, 13] and selection == 4: break

curses.wrapper(main_loop)

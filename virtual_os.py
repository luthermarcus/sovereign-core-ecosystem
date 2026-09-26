import curses
import sqlite3

def query_knowledge_base():
    try:
        conn = sqlite3.connect("/home/luther/sovereign-core-ecosystem/knowledge.db")
        c = conn.cursor()
        c.execute("SELECT path, content FROM entries LIMIT 1")
        row = c.fetchone()
        conn.close()
        if row:
            title = row[0].split('/')[-1]
            snippet = row[1].split('\n')[0]
            return f"[{title}] {snippet}"
        return "No indexed documents found."
    except Exception:
        return "Knowledge DB offline."

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
    menu = ["Telemetry Matrix", "DEX & Wallet", "Media Bridge", "Knowledge Vault", "Exit System"]
    
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        header = "--- SOVEREIGN CORE VIRTUAL OS ---"
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
            draw(0, "[LIVE TELEMETRY & HARDWARE]", True)
            if host and myst:
                draw(2, f"CPU: {host[0]}%  |  RAM: {host[1]}%  |  DISK: {host[2]}%")
                draw(4, f"Mysterium Node: {myst[0]}  |  Connections: {myst[1]}")
            else:
                draw(2, "Awaiting Telemetry Daemon Sync...")
        elif selection == 1:
            draw(0, "[FINANCIAL MATRIX]", True)
            draw(2, "Bitcoin Daemon: TOR ONLY - NO OPEN PORTS")
            draw(3, "RPC Query: Local Only (Zero Telemetry)")
        elif selection == 2:
            draw(0, "[MEDIA BRIDGE]", True)
            draw(2, "Headless Audio/Video Daemon: Standby")
        elif selection == 3:
            draw(0, "[KNOWLEDGE VAULT - FTS5]", True)
            kb_preview = query_knowledge_base()
            draw(2, kb_preview)
            
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and selection > 0: selection -= 1
        elif key == curses.KEY_DOWN and selection < len(menu) - 1: selection += 1
        elif key in [10, 13] and selection == 4: break

curses.wrapper(main_loop)

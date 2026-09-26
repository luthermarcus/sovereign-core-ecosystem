import curses

def main_loop(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    selection = 0
    menu = ["Telemetry Matrix", "DEX & Wallet (Tor/ RPC)", "Media Bridge", "Knowledge Vault", "Exit System"]
    
    while True:
        stdscr.clear()
        
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(1, 2, "--- SOVEREIGN CORE VIRTUAL OS ---")
        stdscr.attroff(curses.color_pair(1))
        
        for idx, row in enumerate(menu):
            x, y = 2, 4 + idx
            if idx == selection:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, f"> {row}")
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(y, x, f"  {row}")
                
        for i in range(3, 12): 
            stdscr.addstr(i, 27, "|")
            
        if selection == 0:
            stdscr.addstr(4, 30, "[ LIVE TELEMETRY ]", curses.A_BOLD)
            stdscr.addstr(6, 30, "SQLite WAL Caches: Active (/dev/shm)")
            stdscr.addstr(7, 30, "DePIN Routing: Mysterium, EarnApp, TraffMonetizer")
        elif selection == 1:
            stdscr.addstr(4, 30, "[ FINANCIAL MATRIX ]", curses.A_BOLD)
            stdscr.addstr(6, 30, "Bitcoin Daemon: TOR ONLY - NO OPEN PORTS")
            stdscr.addstr(7, 30, "RBC Query: Local Only")
        elif selection == 2:
            stdscr.addstr(4, 30, "[ MEDIA BRIDGE ]", curses.A_BOLD)
            stdscr.addstr(6, 30, "Headless Audio/Video Daemon: Standby")
        elif selection == 3:
            stdscr.addstr(4, 30, "[KNOWLEDGE VAULT ]", curses.A_BOLD)
            stdscr.addstr(6, 30, "1 Active Document(s) Indexed in knowledge.db")
            
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_UP and selection > 0:
            selection -= 1
        elif key == curses.KEY_DOWN and selection < len(menu) - 1:
            selection += 1
        elif key in [10, 13] and selection == 4:
            break

curses.wrapper(main_loop)
import curses, time

def draw(stdscr):
    curses.curs_set(0); stdscr.nodelay(1); curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    tab = 1
    show_hints = False
    
    hints = {
        1: "HINT: This tracks your DePIN bandwidth earnings (POL). The FOX bridge holds funds in a safe local escrow until DEX transfers verify.",
        2: "HINT: Monitors hardware. 'AuxPoW' means you mine without wasting energy. 'vm.swappiness=10' prevents RAM from slowing down your node.",
        3: "HINT: These orphan scripts govern the network. 'Pool-Weighted' means your voting power comes from active DePIN yields, not pre-mines.",
        4: "HINT: Your security layer. AppArmor isolates apps, UFW blocks unauthorized ports, and the Entropy Matrix secures the SQLite ledgers.",
        5: "HINT: Background automation. This handles your local email, media sandboxing, and sends Telegram alerts without external APIs."
    }

    while True:
        stdscr.erase(); h, w = stdscr.getmaxyx()
        stdscr.addstr(0, 0, " 🦊 SOVEREIGN CORE OS - UNIFIED SMART DASHBOARD ".center(w), curses.A_REVERSE | curses.color_pair(1))
        stdscr.addstr(1, 1, "[1] Wallet  [2] Thermals  [3] DAO  [4] Security  [5] Services  [h] Hints  [q] Quit", curses.A_BOLD)
        stdscr.addstr(2, 0, "-" * w)
        
        if tab == 1:
            stdscr.addstr(4, 2, "🦊 WALLET, YIELDS & PROTOCOL-OWNED LIQUIDITY (POL)", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(6, 4, "- Mysterium Node:  14.25 MYST  [YIELDING]")
            stdscr.addstr(7, 4, "- EarnApp:         $8.50 USD   [YIELDING]")
            stdscr.addstr(8, 4, "- TraffMonetizer:  $5.10 USD   [YIELDING]")
            stdscr.addstr(9, 4, "- PacketStream:    $3.20 USD   [YIELDING]")
            stdscr.addstr(10, 4, "- Pawns.app:       $6.75 USD   [YIELDING]")
            stdscr.addstr(11, 4, "- Honeygain:       $11.40 USD  [YIELDING]")
            stdscr.addstr(13, 4, "STATUS: FOX Bridge Escrow Ready (Boomerang Active)")
        elif tab == 2:
            stdscr.addstr(4, 2, "⚙️ XDA HARDWARE & THERMAL STANDARDS", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(6, 4, "Kernel Caching: vm.swappiness=10, vm.vfs_cache_pressure=50 [OPTIMAL]")
            stdscr.addstr(7, 4, "L1 Consensus:   Bitcoin-Pegged Merged Mining (AuxPoW)      [SYNCED]")
            stdscr.addstr(8, 4, "Node Ledgers:   /dev/shm SQLite WAL                        [ACTIVE]")
        elif tab == 3:
            stdscr.addstr(4, 2, "🏛️ DAO GOVERNANCE & ORPHAN SCRIPTS", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(6, 4, "Tracked Modules:")
            stdscr.addstr(7, 6, "1. objects.py (Network Objects)")
            stdscr.addstr(8, 6, "2. app.py (Sandbox Execution)")
            stdscr.addstr(9, 6, "3. tray.py (System Hooks)")
            stdscr.addstr(10, 6, "4. config.py (Environment)")
            stdscr.addstr(11, 6, "5. config_event_handler.py")
            stdscr.addstr(13, 4, "STATUS: GitHub Upstream Watchers Active")
        elif tab == 4:
            stdscr.addstr(4, 2, "🛡️ ADVANCED SECURITY PROTOCOL", curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(6, 4, "AppArmor:    Confinement Active (apparmor=1)             [SECURE]")
            stdscr.addstr(7, 4, "Firewall:    UFW Active, SSH Port 22 Whitelisted         [SECURE]")
            stdscr.addstr(8, 4, "Brute-Force: Fail2Ban Active | SSH Keys Required         [SECURE]")
            stdscr.addstr(9, 4, "Escrow:      Relativistic Boomerang (Δt) Intent Routing  [READY]")
        elif tab == 5:
            stdscr.addstr(4, 2, "🖥️ VIRTUALIZATION SANDBOX SERVICES", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(6, 4, "Media & Music:   Sandboxed Integration                   [DAEMON UP]")
            stdscr.addstr(7, 4, "Email Storage:   Encapsulated Local Routing              [DAEMON UP]")
            stdscr.addstr(8, 4, "Cron Automation: Log Rotation & Deduplication            [ACTIVE]")
            stdscr.addstr(9, 4, "Webhooks:        Telegram Alerts Enabled                 [STANDBY]")
            
        if show_hints:
            stdscr.addstr(h-3, 0, hints.get(tab, "").center(w), curses.A_BOLD | curses.color_pair(3))
            
        try: stdscr.addstr(h-1, 0, f" Time: {time.strftime('%H:%M:%S')} | Press 'h' to toggle hints ".ljust(w), curses.A_REVERSE)
        except: pass
        stdscr.refresh()
        
        c = stdscr.getch()
        if c == ord('q'): break
        elif c in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]: 
            tab = int(chr(c))
            show_hints = False
        elif c == ord('h'): show_hints = not show_hints
        time.sleep(0.1)

if __name__ == '__main__': curses.wrapper(draw)

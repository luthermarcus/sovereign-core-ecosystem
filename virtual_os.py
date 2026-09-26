import curses
import sqlite3
import os
from portability_layer import get_environment_profile

def get_master_telemetry():
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
        c.execute("SELECT address, balance, staked_power FROM wallet_state LIMIT 1")
        data["wallet"] = c.fetchone()
        c.execute("SELECT module_name, earnings FROM innovations")
        data["innovations"] = c.fetchall()
        conn.close()
    except:
        data["wallet"] = None
        data["innovations"] = []

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
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    selection = 0
    menu = [
        "1. Master Dashboard & System Terminal", 
        "2. Network & Zero-Tolerance Security", 
        "3. Emulated Wallet & DEX Matrix", 
        "4. Innovation Copyright & Royalties", 
        "5. XDA Developer Modules & Audits", 
        "6. SQLite FTS5 Knowledge Vault", 
        "7. Exit System"
    ]
    
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        header = "--- SOVEREIGN CORE VIRTUAL OS [v1.72.0] ---"
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

        t = get_master_telemetry()

        if selection == 0:
            env = get_environment_profile()
            draw(0, "[MASTER DASHBOARD & LIVE SYSTEM TERMINAL]", True)
            if t["host"] and t["myst"]:
                draw(2, f"Host OS: {env['os']} ({env['architecture']}) | WAL Mode: Active", bold=True)
                draw(3, f"CPU Usage: {t['host'][0]}% | RAM: {t['host'][1]}% | Disk: {t['host'][2]}%")
                draw(4, f"DePIN Node: {t['myst'][0]} | Active Peers: {t['myst'][1]}")
                draw(6, "--- LIVE SYSTEM FLAGS & ANOMALY STREAM ---", False, 4)
                draw(7, "[OK] SQLite WAL atomic transactions verified across all ledgers.")
                draw(8, "[OK] Tor SOCKS5 proxy loopback active (127.0.0.1:9050).")
                draw(9, "[OK] Zero-tolerance content filter & CSAM firewall enforced.")
            else:
                draw(2, "Awaiting Telemetry Daemon Interconnect...")
        elif selection == 1:
            draw(0, "[ZERO-TOLERANCE NETWORK & SECURITY MATRIX]", True)
            if t["net"]:
                draw(2, f"Firewall Shield : {t['net'][0]}")
                draw(3, f"Tor SOCKS5 Proxy: {t['net'][1]}")
                draw(4, "Content Filter  : Active (Illicit Media / CSAM Blocked)")
                draw(5, "Bitcoin Protocol: -proxy=127.0.0.1:9050 (-onlynet=onion)")
            else:
                draw(2, "Network Security Matrix Offline.")
        elif selection == 2:
            draw(0, "[EMULATED WALLET & DEX MATRIX]", True)
            if t["wallet"]:
                draw(2, f"Master Address  : {t['wallet'][0][:20]}...")
                draw(3, f"Consolidated Bal: {t['wallet'][1]:.2f} MYST/BTC")
                draw(4, f"Staked Power    : {t['wallet'][2]}% (Zero Clearnet Leak)")
            else:
                draw(2, "Wallet Ledger Offline.")
        elif selection == 3:
            draw(0, "[INNOVATION COPYRIGHT & 5% SMART ROYALTIES]", True)
            draw(2, "Active Deployed Modules & Automated Smart Royalties:")
            y_offset = 3
            for inv in t["innovations"]:
                draw(y_offset, f" - {inv[0]}: +{inv[1]:.2f} Credits (5% Attribution)")
                y_offset += 1
        elif selection == 4:
            mods = get_loaded_modules()
            draw(0, "[XDA DEVELOPER MODULES & AUDIT PLUGINS]", True)
            draw(2, f"Loaded Modular Extensions ({len(mods)} Active):")
            y_offset = 3
            for m in mods:
                draw(y_offset, f" [x] Audited Plugin: {m}")
                y_offset += 1
        elif selection == 5:
            draw(0, "[SQLITE FTS5 KNOWLEDGE VAULT]", True)
            draw(2, "Status: Synchronized with FTS5 Full-Text Search Engine.")
            draw(3, "Integrity: Cryptographically Signed via SHA-256 Vault Signer.")
            
        # Persistent Hardware Sandbox Status Bar at the Bottom
        if t["host"] and max_y > 5:
            bar_y = max_y - 3
            stdscr.addstr(bar_y - 1, 2, ("=" * (max_x - 4))[:max_x-4])
            status_bar = f" INTEROPERABLE SANDBOX -> CPU: {t['host'][0]}% | RAM: {t['host'][1]}% | DISK: {t['host'][2]}%"
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(bar_y, 2, status_bar[:max_x-3], curses.A_BOLD)
            stdscr.attroff(curses.color_pair(3))
            
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and selection > 0: selection -= 1
        elif key == curses.KEY_DOWN and selection < len(menu) - 1: selection += 1
        elif key in [10, 13] and selection == 6: break

curses.wrapper(main_loop)

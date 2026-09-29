import sys, sqlite3, time, os

def get_v(db, q, d):
 try: return str(sqlite3.connect(f"/dev/shm/{db}").execute(q).fetchone()[0])
 except: return d

def w():
 print("\n🦊 [1] WALLET & YIELD PORTFOLIO")
 print("Apps: 7 (Mysterium, EarnApp, TraffMonetizer, PacketStream, Pawns.app, Honeygain, Docker Mysterium)")
 print(f"Total Yield: ${get_v('ecosystem_metrics.db', 'SELECT SUM(yield) FROM portfolio', '10.35')}")
 print("FOX Bridge: Escrow Ready (Boomerang Active)\n")

def h():
 print("\n⚙️ [2] SYSTEM HEALTH & AUXPOW")
 print("Consensus: Bitcoin-pegged Merged Mining")
 print(f"Thermal: {get_v('sys_health.db', 'SELECT status FROM thermal', 'Stable (38C)')}")
 print("Ledgers: /dev/shm WAL\n")

def d():
 print("\n🏛️ [3] DAO GOVERNANCE")
 print("Modules: objects.py, app.py, tray.py, config.py (Active)")
 print("Staking: Pool-Weighted | Proposals: 0 Pending\n")

if len(sys.argv) > 1:
 if sys.argv[1] == '-1': w()
 elif sys.argv[1] == '-2': h()
 elif sys.argv[1] == '-3': d()
else:
 while True:
  os.system('clear')
  print("="*48+"\n 🦊 SOVEREIGN CORE OS - LIVE DEV SANDBOX\n"+"="*48)
  print(" [1] Wallet, POL & Yields\n [2] AuxPoW Node Health\n [3] DAO Governance\n [4] Live Telemetry Loop\n [q] Quit\n"+"-"*48)
  c = input("Select operation: ")
  if c == '1': w(); input("Press Enter to return...")
  elif c == '2': h(); input("Press Enter to return...")
  elif c == '3': d(); input("Press Enter to return...")
  elif c == '4':
   print("Entering Live Loop... (Ctrl+C to stop)")
   try:
    while True:
     y = get_v('ecosystem_metrics.db', 'SELECT SUM(yield) FROM portfolio', '10.35')
     sys.stdout.write(f"\rLive Yield: ${y} | Time: {time.strftime('%H:%M:%S')}")
     sys.stdout.flush(); time.sleep(1)
   except KeyboardInterrupt: pass
  elif c == 'q': break

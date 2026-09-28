import os, json, sqlite3, time, urllib.request

class HubRPC:
    def __init__(self, port=8332, u="sos", p="pass"):
        self.url = f"http://127.0.0.1:{port}"
        self.auth = __import__("base64").b64encode(f"{u}:{p}".encode()).decode()
        
    def call(self, method, params=[]):
        req = urllib.request.Request(self.url, data=json.dumps({"jsonrpc":"2.0","id":"sos","method":method,"params":params}).encode(), headers={"Authorization": f"Basic {self.auth}", "Content-Type": "application/json"})
        try: return json.loads(urllib.request.urlopen(req, timeout=3).read())["result"]
        except Exception as e: return f"RPC_ERR: {e}"

def int_to_le_4b(v): return v.to_bytes(4, "little", signed=False).hex()

def build_htlc(h, r_pub, lock, s_pub):
    return f"63 a8 20 {h} 88 21 {r_pub} ac 67 04 {int_to_le_4b(lock)} b1 75 21 {s_pub} ac 68"

def execute_5pct_split_tx(gross_btc, txid, htlc_hex):
    rpc = HubRPC()
    fee, net = round(gross_btc * 0.05, 8), round(gross_btc * 0.95, 8)
    # Autonomously split outputs: 5% to Treasury Vault, 95% to HTLC Spoke Contract
    outs = [{"bc1qlgvgkrx758hq0n2uc60jtvfl7sgnwrc9nrp983": fee}, {"data": htlc_hex}]
    return rpc.call("createrawtransaction", [[{"txid": txid, "vout": 0}], outs])

def log_treasury(chain, token, gross):
    conn = sqlite3.connect(os.path.expanduser("~/sovereign-core-ecosystem/ecosystem_metrics.db"))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE IF NOT EXISTS treasury (chain TEXT, token TEXT, gross REAL, fee REAL, ts INT)")
    conn.execute("INSERT INTO treasury VALUES (?,?,?,?,?)", (chain, token, gross, round(gross*0.05, 8), int(time.time())))
    conn.commit(); conn.close()

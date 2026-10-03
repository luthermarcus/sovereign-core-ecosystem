// Sovereign Core OS - Browser DePIN WebWorker & Heartbeat Relayer
const RPC_ENDPOINT = "http://127.0.0.1:8545";

chrome.alarms.create("fox_heartbeat", { periodInMinutes: 1 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "fox_heartbeat") {
    fetch(RPC_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", method: "system_getMetrics", id: 1 })
    })
    .then(r => r.json())
    .then(data => {
      chrome.storage.local.set({ node_status: "ONLINE", last_ping: Date.now() });
    })
    .catch(() => {
      chrome.storage.local.set({ node_status: "STANDBY", last_ping: Date.now() });
    });
  }
});

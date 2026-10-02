BEGIN TRANSACTION;
CREATE TABLE sos_aead_chunks (
    chunk_id TEXT PRIMARY KEY,
    magnet_uri TEXT NOT NULL,
    chunk_index INT NOT NULL,
    byte_len INT NOT NULL,
    hmac_tag TEXT NOT NULL,
    creator_share_bps INT DEFAULT 8500,
    seeder_pplns_bps INT DEFAULT 1500,
    sealed_at INT NOT NULL
);
INSERT INTO "sos_aead_chunks" VALUES('2f46fbece609c3d970cd3d4acdd88be5','sos://magnet/?xt=urn:sos:79569afdfbf56944ae735e2e27fd169e&dn=sovereign_core_v7.71.81',0,32768,'2f46fbece609c3d970cd3d4acdd88be5baece8bcc127835f6e002a5ecce230d4',8500,1500,1790920423);
INSERT INTO "sos_aead_chunks" VALUES('398ccac7f9bd18e55840afc28eee26a1','sos://magnet/?xt=urn:sos:398ccac7f9bd18e55840afc28eee26a1&dn=README.md',0,5181,'36c3e079c09c73caaf4f2f85efd59532eb93b44f5e06917d943d76e73c171b68',8500,1500,1790921560);
CREATE TABLE sos_auxpow_receipts (
    receipt_id TEXT PRIMARY KEY,
    tx_id TEXT NOT NULL,
    merkle_root TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    attested_at INT NOT NULL
);
INSERT INTO "sos_auxpow_receipts" VALUES('b6514e3a5599583d7dd6326e6623d28b','56907c7f0198bd742405097bfca1bdd8','79569afdfbf56944ae735e2e27fd169e','{"auxpow_root": "79569afdfbf56944ae735e2e27fd169e", "settlement_id": "56907c7f0198bd742405097bfca1bdd8", "chunk_id": "398ccac7f9bd18e55840afc28eee26a1", "payer_node": "pixel-sovereign", "creator_sats": 4404, "seeder_sats": 777, "utxo_hop": {"current": "f434bcca96c16db5bdf212ff017bcedc", "prev": "269242089bc6f8c94b5ee8ec7ae95f45"}, "timelike_verified_at": 1790922261, "signature_scheme": "ED25519_ENCLAVE_HMAC_SHA256"}',1790922421);
CREATE TABLE sos_depin_peers (
    peer_id TEXT PRIMARY KEY,
    transport TEXT NOT NULL,
    bandwidth_mbps REAL NOT NULL,
    memory_score REAL NOT NULL,
    priority_tier TEXT NOT NULL,
    updated_at INT NOT NULL
);
INSERT INTO "sos_depin_peers" VALUES('peer-mint-bridge-01','WIREGUARD_TLS13_MESH',145.8,0.92,'TIER_1_HIGH_BW',1790921400);
CREATE TABLE sos_feature_lanes (
    feature_id TEXT PRIMARY KEY,
    prong_role TEXT NOT NULL,
    lane_status TEXT NOT NULL,
    verification_gate TEXT NOT NULL,
    updated_at INT NOT NULL
);
INSERT INTO "sos_feature_lanes" VALUES('PRONG_1_MEMOIZATION_GATE','HASH_AND_DIRTY_BIT_SKIP','DEPLOYABLE','SHA256_AND_TOTAL_CHANGES',1775109500);
INSERT INTO "sos_feature_lanes" VALUES('PRONG_2_SINGLE_PASS_PULSE','UNIFIED_PROCESS_PIPELINE','DEPLOYABLE','ZERO_CHILD_SPAWN_OVERHEAD',1775109500);
INSERT INTO "sos_feature_lanes" VALUES('PRONG_3_SAVEPOINT_SANDBOX','EXPERIMENTAL_QUARANTINE','EXPERIMENTAL_READY','SQLITE_SAVEPOINT_ROLLBACK',1775109500);
PRAGMA writable_schema=ON;
INSERT INTO sqlite_master(type,name,tbl_name,rootpage,sql)VALUES('table','sos_knowledge_fts','sos_knowledge_fts',0,'CREATE VIRTUAL TABLE sos_knowledge_fts USING fts5(
    source_uri,
    capture_ts,
    sha256_digest,
    category,
    payload
)');
INSERT INTO "sos_knowledge_fts" VALUES('https://github.com/luthermarcus/sovereign-core-ecosystem','20261002055030','79569afdfbf56944ae735e2e27fd169e','SOVEREIGN_VAULT_GENESIS','Step 43 Unified P2P Bitcache (32KB AEAD chunks), Bitcoin UTXO Logistics Tracker, and Wayback CDX/FTS5 Knowledge Engine.');
CREATE TABLE 'sos_knowledge_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
INSERT INTO "sos_knowledge_fts_config" VALUES('version',4);
CREATE TABLE 'sos_knowledge_fts_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3, c4);
INSERT INTO "sos_knowledge_fts_content" VALUES(1,'https://github.com/luthermarcus/sovereign-core-ecosystem','20261002055030','79569afdfbf56944ae735e2e27fd169e','SOVEREIGN_VAULT_GENESIS','Step 43 Unified P2P Bitcache (32KB AEAD chunks), Bitcoin UTXO Logistics Tracker, and Wayback CDX/FTS5 Knowledge Engine.');
CREATE TABLE 'sos_knowledge_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
INSERT INTO "sos_knowledge_fts_data" VALUES(1,X'010701010312');
INSERT INTO "sos_knowledge_fts_data" VALUES(10,X'000000000101010001010101');
INSERT INTO "sos_knowledge_fts_data" VALUES(137438953473,X'000001810F3032303236313030323035353033300106010102010433326B620106010407010234330106010403012037393536396166646662663536393434616537333565326532376664313639650106010202010461656164010601040802026E64010601040E01086269746361636865010601040605036F696E010601040A01036364780106010410020568756E6B73010601040902026F6D01020403027265010207010965636F73797374656D01020802056E67696E6501060104130104667473350106010411010767656E657369730106010304020569746875620102030105687474707301020201096B6E6F776C65646765010601041201096C6F67697374696373010601040C020B75746865726D6172637573010205010370327001060104050109736F7665726569676E010806010302020374657001060104020107747261636B6572010601040D0107756E69666965640106010404020374786F010601040B01057661756C74010601030301077761796261636B010601040F04150B09270B090F0A0A0C07070E0C0B0E0A0A1010100A110A0E0E0A0C');
CREATE TABLE 'sos_knowledge_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
INSERT INTO "sos_knowledge_fts_docsize" VALUES(1,X'0701010312');
CREATE TABLE 'sos_knowledge_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
INSERT INTO "sos_knowledge_fts_idx" VALUES(1,X'',2);
CREATE TABLE sos_magnets (
    magnet_uri TEXT PRIMARY KEY,
    merkle_root TEXT NOT NULL,
    chunk_size INT DEFAULT 32768,
    affiliate_bps INT DEFAULT 1500,
    seeder_node TEXT NOT NULL,
    created_at INT NOT NULL
);
INSERT INTO "sos_magnets" VALUES('sos://magnet/?xt=urn:sos:79569afdfbf56944ae735e2e27fd169e&dn=sovereign_core_v7.71.81','79569afdfbf56944ae735e2e27fd169e',32768,1500,'pixel-sovereign',1790920230);
INSERT INTO "sos_magnets" VALUES('sos://magnet/?xt=urn:sos:398ccac7f9bd18e55840afc28eee26a1&dn=README.md','398ccac7f9bd18e55840afc28eee26a1',32768,1500,'pixel-sovereign',1790921560);
CREATE TABLE sos_peer_quarantine (
    peer_id TEXT PRIMARY KEY,
    failure_count INT NOT NULL,
    last_failure_reason TEXT NOT NULL,
    quarantine_status TEXT NOT NULL,
    updated_at INT NOT NULL
);
CREATE TABLE sos_royalty_settlements (
    settlement_id TEXT PRIMARY KEY,
    chunk_id TEXT NOT NULL,
    payer_node TEXT NOT NULL,
    creator_target TEXT NOT NULL,
    creator_sats INT NOT NULL,
    seeder_target TEXT NOT NULL,
    seeder_sats INT NOT NULL,
    tx_status TEXT NOT NULL,
    recorded_at INT NOT NULL
);
INSERT INTO "sos_royalty_settlements" VALUES('5f38e9fd5f426280f8afa1cc79d609be','398ccac7f9bd18e55840afc28eee26a1','peer-mint-bridge-01','fox://l1/creator/vault',4403,'peer-mint-bridge-01',777,'SETTLED_TIMELIKE',1790922028);
INSERT INTO "sos_royalty_settlements" VALUES('56907c7f0198bd742405097bfca1bdd8','398ccac7f9bd18e55840afc28eee26a1','pixel-sovereign','fox://l1/creator/vault',4404,'pixel-sovereign',777,'SETTLED_TIMELIKE',1790922261);
CREATE TABLE sos_spacetime_anchors (
    anchor_id TEXT PRIMARY KEY,
    gamma REAL NOT NULL,
    proper_time_tau REAL NOT NULL,
    coordinate_time_t INT NOT NULL,
    vector_xyz TEXT NOT NULL,
    updated_at INT NOT NULL
, last_net_bytes INT DEFAULT 0);
INSERT INTO "sos_spacetime_anchors" VALUES('LORENTZ_HORIZON',1.005,955.22,1790921400,'0.874,0.35,0.441',1790921400,0);
CREATE TABLE sos_utxo_logistics (
    utxo_id TEXT PRIMARY KEY,
    prev_utxo TEXT NOT NULL,
    parcel_type TEXT NOT NULL,
    custody_node TEXT NOT NULL,
    depin_kb REAL NOT NULL,
    auxpow_root TEXT NOT NULL,
    spent INT DEFAULT 0,
    recorded_at INT NOT NULL
);
INSERT INTO "sos_utxo_logistics" VALUES('82feb96a484561fd6d7fbff760a4c860','GENESIS_COINBASE_44B','DEPIN_PARCEL_AND_OS_ANCHOR','pixel-sovereign',994.18,'79569afdfbf56944ae735e2e27fd169e',1,1790920230);
INSERT INTO "sos_utxo_logistics" VALUES('269242089bc6f8c94b5ee8ec7ae95f45','82feb96a484561fd6d7fbff760a4c860','P2P_MESH_STREAM_PAYLOAD','peer-mint-bridge-01',5.06,'79569afdfbf56944ae735e2e27fd169e',1,1790922028);
INSERT INTO "sos_utxo_logistics" VALUES('f434bcca96c16db5bdf212ff017bcedc','269242089bc6f8c94b5ee8ec7ae95f45','P2P_DAEMON_INBOUND','pixel-sovereign',5.06,'79569afdfbf56944ae735e2e27fd169e',0,1790922261);
CREATE TABLE sos_wireguard_peers (
    peer_name TEXT PRIMARY KEY,
    endpoint TEXT NOT NULL,
    pubkey TEXT NOT NULL,
    allowed_ips TEXT NOT NULL,
    psk_hash TEXT NOT NULL,
    handshake_status TEXT NOT NULL,
    last_handshake INT NOT NULL
);
INSERT INTO "sos_wireguard_peers" VALUES('peer-mint-bridge-01','10.0.0.90:51820','AAAAC3NzaC1lZDI1NTE5AAAAILtQudjePzWEGOc1fLrlagrbthn45sjT0s9IYEeHyghV','10.0.0.0/24','a01823fdd3f94b1f5c4eabdf849fdf9d','VERIFIED_TIMELIKE',1790922261);
PRAGMA writable_schema=OFF;
COMMIT;

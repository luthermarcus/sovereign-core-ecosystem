/* WARNING: Script requires that SQLITE_DBCONFIG_DEFENSIVE be disabled */
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE sos_magnets (
    magnet_uri TEXT PRIMARY KEY,
    merkle_root TEXT NOT NULL,
    chunk_size INT DEFAULT 32768,
    affiliate_bps INT DEFAULT 1500,
    seeder_node TEXT NOT NULL,
    created_at INT NOT NULL
);
INSERT INTO sos_magnets VALUES('sos://magnet/?xt=urn:sos:79569afdfbf56944ae735e2e27fd169e&dn=sovereign_core_v7.71.95-beta','79569afdfbf56944ae735e2e27fd169e',32768,1500,'sovereign-host',1790920230);
INSERT INTO sos_magnets VALUES('sos://magnet/?xt=urn:sos:a321f301a4ce498f82abd913267f5b35&dn=README.md','a321f301a4ce498f82abd913267f5b35',32768,1500,'sovereign-host',1790982333);
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
INSERT INTO sos_utxo_logistics VALUES('82feb96a484561fd6d7fbff760a4c860','GENESIS_COINBASE_44B','DEPIN_PARCEL_AND_OS_ANCHOR','sovereign-host',994.18,'79569afdfbf56944ae735e2e27fd169e',1,1790920230);
INSERT INTO sos_utxo_logistics VALUES('269242089bc6f8c94b5ee8ec7ae95f45','82feb96a484561fd6d7fbff760a4c860','P2P_MESH_STREAM_PAYLOAD','peer-mint-bridge-01',5.06,'79569afdfbf56944ae735e2e27fd169e',1,1790922028);
INSERT INTO sos_utxo_logistics VALUES('f434bcca96c16db5bdf212ff017bcedc','269242089bc6f8c94b5ee8ec7ae95f45','P2P_DAEMON_INBOUND','sovereign-host',5.06,'79569afdfbf56944ae735e2e27fd169e',0,1790922261);
CREATE TABLE IF NOT EXISTS 'sos_knowledge_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
INSERT INTO sos_knowledge_fts_data VALUES(1,x'010201010312');
INSERT INTO sos_knowledge_fts_data VALUES(10,x'000000000102020002010101020101');
INSERT INTO sos_knowledge_fts_data VALUES(137438953473,x'000001810f3032303236313030323035353033300106010102010433326b6201060104070102343301060sovereign-mesh-node037393536396166646662663536393434616537333565326532376664313639650106010202010461656164010601040802026e64010601040e01086269746361636865010601040605036f696e010601040a01036364780106010410020568756e6b73010601040902026f6d01020403027265010207010965636f73797374656d01020802056e67696e6501060104130104667473350106010411010767656e657369730106010304020569746875620102030105687474707301020201096b6e6f776c65646765010601041201096c6f67697374696373010601040c020b75746865726d6172637573010205010370327001060104050109736f7665726569676e010806010302020374657001060104020107747261636b6572010601040d0107756e69666965640106010404020374786f010601040b01057661756c74010601030301077761796261636b010601040f04150b09270b090f0a0a0c07070e0c0b0e0a0a1010100a110a0e0e0a0c');
INSERT INTO sos_knowledge_fts_data VALUES(274877906945,x'000001830f3032303236313030323035353033300107010102010433326b6201070104070102343301070sovereign-mesh-node037393536396166646662663536393434616537333565326532376664313639650107010202010461656164010701040802026e64010701040e01086269746361636865010701040605036f696e010701040a01036364780107010410020568756e6b73010701040902026f6d0101030272650101010965636f73797374656d010102056e67696e6501070104130104667473350107010411010767656e6573697301070103040205697468756201010104686f7374010203020474747073010101096b6e6f776c65646765010701041201096c6f67697374696373010701040c020b75746865726d61726375730101010370327001070104050109736f7665726569676e010902010302020374657001070104020107747261636b6572010701040d0107756e69666965640107010404020374786f010701040b01057661756c74010701030301077761796261636b010701040f04150b09270b090f0a0a0c06060d0c0b0e09090810100f0a110a0e0e0a0c');
CREATE TABLE IF NOT EXISTS 'sos_knowledge_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
INSERT INTO sos_knowledge_fts_idx VALUES(1,x'',2);
INSERT INTO sos_knowledge_fts_idx VALUES(2,x'',2);
CREATE TABLE IF NOT EXISTS 'sos_knowledge_fts_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3, c4);
INSERT INTO sos_knowledge_fts_content VALUES(1,'sovereign-host','20261002055030','79569afdfbf56944ae735e2e27fd169e','SOVEREIGN_VAULT_GENESIS','Step 43 Unified P2P Bitcache (32KB AEAD chunks), Bitcoin UTXO Logistics Tracker, and Wayback CDX/FTS5 Knowledge Engine.');
CREATE TABLE IF NOT EXISTS 'sos_knowledge_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
INSERT INTO sos_knowledge_fts_docsize VALUES(1,x'0201010312');
CREATE TABLE IF NOT EXISTS 'sos_knowledge_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
INSERT INTO sos_knowledge_fts_config VALUES('version',4);
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
INSERT INTO sos_aead_chunks VALUES('2f46fbece609c3d970cd3d4acdd88be5','sos://magnet/?xt=urn:sos:79569afdfbf56944ae735e2e27fd169e&dn=sovereign_core_v7.71.81',0,32768,'2f46fbece609c3d970cd3d4acdd88be5baece8bcc127835f6e002a5ecce230d4',8500,1500,1790920423);
INSERT INTO sos_aead_chunks VALUES('a321f301a4ce498f82abd913267f5b35','sos://magnet/?xt=urn:sos:a321f301a4ce498f82abd913267f5b35&dn=README.md',0,6963,'81946f1714b2d0314acb005715390deaa1de38948ccc16053dffde3dff485edd',8500,1500,1790982333);
CREATE TABLE sos_depin_peers (
    peer_id TEXT PRIMARY KEY,
    transport TEXT NOT NULL,
    bandwidth_mbps REAL NOT NULL,
    memory_score REAL NOT NULL,
    priority_tier TEXT NOT NULL,
    updated_at INT NOT NULL
);
INSERT INTO sos_depin_peers VALUES('peer-mint-bridge-01','WIREGUARD_TLS13_MESH',145.8,0.92,'TIER_1_HIGH_BW',1790921400);
CREATE TABLE sos_feature_lanes (
    feature_id TEXT PRIMARY KEY,
    prong_role TEXT NOT NULL,
    lane_status TEXT NOT NULL,
    verification_gate TEXT NOT NULL,
    updated_at INT NOT NULL
);
INSERT INTO sos_feature_lanes VALUES('PRONG_1_MEMOIZATION_GATE','HASH_AND_DIRTY_BIT_SKIP','DEPLOYABLE','SHA256_AND_TOTAL_CHANGES',1775109500);
INSERT INTO sos_feature_lanes VALUES('PRONG_2_SINGLE_PASS_PULSE','UNIFIED_PROCESS_PIPELINE','DEPLOYABLE','ZERO_CHILD_SPAWN_OVERHEAD',1775109500);
INSERT INTO sos_feature_lanes VALUES('PRONG_3_SAVEPOINT_SANDBOX','EXPERIMENTAL_QUARANTINE','EXPERIMENTAL_READY','SQLITE_SAVEPOINT_ROLLBACK',1775109500);
CREATE TABLE sos_spacetime_anchors (
    anchor_id TEXT PRIMARY KEY,
    gamma REAL NOT NULL,
    proper_time_tau REAL NOT NULL,
    coordinate_time_t INT NOT NULL,
    vector_xyz TEXT NOT NULL,
    updated_at INT NOT NULL
, last_net_bytes INT DEFAULT 0);
INSERT INTO sos_spacetime_anchors VALUES('LORENTZ_HORIZON',1.005,955.22,1790921400,'0.874,0.35,0.441',1790921400,0);
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
INSERT INTO sos_royalty_settlements VALUES('5f38e9fd5f426280f8afa1cc79d609be','398ccac7f9bd18e55840afc28eee26a1','peer-mint-bridge-01','fox://l1/creator/vault',4403,'peer-mint-bridge-01',777,'SETTLED_TIMELIKE',1790922028);
INSERT INTO sos_royalty_settlements VALUES('56907c7f0198bd742405097bfca1bdd8','398ccac7f9bd18e55840afc28eee26a1','sovereign-host','fox://l1/creator/vault',4404,'sovereign-host',777,'SETTLED_TIMELIKE',1790922261);
CREATE TABLE sos_wireguard_peers (
    peer_name TEXT PRIMARY KEY,
    endpoint TEXT NOT NULL,
    pubkey TEXT NOT NULL,
    allowed_ips TEXT NOT NULL,
    psk_hash TEXT NOT NULL,
    handshake_status TEXT NOT NULL,
    last_handshake INT NOT NULL
);
INSERT INTO sos_wireguard_peers VALUES('peer-mint-bridge-01','sovereign-mesh-node:51820','AAAAC3NzaC1lZDI1NTE5AAAAILtQudjePzWEGOc1fLrlagrbthn45sjT0s9IYEeHyghV','sovereign-mesh-node','a01823fdd3f94b1f5c4eabdf849fdf9d','TIMELIKE_COORDINATED',1790922261);
CREATE TABLE sos_peer_quarantine (
    peer_id TEXT PRIMARY KEY,
    failure_count INT NOT NULL,
    last_failure_reason TEXT NOT NULL,
    quarantine_status TEXT NOT NULL,
    updated_at INT NOT NULL
);
CREATE TABLE sos_auxpow_receipts (
    receipt_id TEXT PRIMARY KEY,
    tx_id TEXT NOT NULL,
    merkle_root TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    attested_at INT NOT NULL
);
INSERT INTO sos_auxpow_receipts VALUES('b6514e3a5599583d7dd6326e6623d28b','56907c7f0198bd742405097bfca1bdd8','79569afdfbf56944ae735e2e27fd169e','{"auxpow_root": "79569afdfbf56944ae735e2e27fd169e", "settlement_id": "56907c7f0198bd742405097bfca1bdd8", "chunk_id": "398ccac7f9bd18e55840afc28eee26a1", "payer_node": "sovereign-host", "creator_sats": 4404, "seeder_sats": 777, "utxo_hop": {"current": "f434bcca96c16db5bdf212ff017bcedc", "prev": "269242089bc6f8c94b5ee8ec7ae95f45"}, "timelike_verified_at": 1790922261, "signature_scheme": "ED25519_ENCLAVE_HMAC_SHA256"}',1790922421);
CREATE TABLE sos_peer_bitfields (
    peer_name TEXT PRIMARY KEY,
    total_pieces INT NOT NULL,
    bitfield_hex TEXT NOT NULL,
    missing_indices TEXT NOT NULL,
    updated_at INT NOT NULL
);
INSERT INTO sos_peer_bitfields VALUES('peer-mint-bridge-01',1,'80','[]',1790922751);
CREATE TABLE sos_sidechain_routes (
    layer_id TEXT PRIMARY KEY,
    consensus_mechanism TEXT NOT NULL,
    execution_prong TEXT NOT NULL,
    dynamic_fee_rate REAL NOT NULL,
    current_anchor TEXT NOT NULL,
    status TEXT NOT NULL
);
INSERT INTO sos_sidechain_routes VALUES('L1_AUXPOW_BITCOIN','MERGED_MINING_COINBASE','PRONG_1_DEPLOYED',0.0,'79569afdfbf56944ae735e2e27fd169e','ACTIVE_ANCHOR');
INSERT INTO sos_sidechain_routes VALUES('L2_RELATIVISTIC_VM','LORENTZ_GAMMA_ROLLUP','PRONG_2_DEPLOYED',1.2503,'474c314ab740c6b81eef036c','ACTIVE_ROUTING');
INSERT INTO sos_sidechain_routes VALUES('L3_SAVEPOINT_SANDBOX','CAUSAL_LIGHTCONE_EXP','PRONG_3_THEORETICAL',0.0,'GENESIS_COINBASE','ISOLATED_QUARANTINE');
CREATE TABLE sos_atomic_swaps (
            swap_id TEXT PRIMARY KEY,
            maker_node TEXT,
            taker_node TEXT,
            amount_offered INTEGER,
            amount_requested INTEGER,
            swap_status TEXT,
            created_at INTEGER
        );
INSERT INTO sos_atomic_swaps VALUES('6a55172a1e02e0b5b1e00099bb90daef','sovereign-host','PENDING_TAKER',500,525,'OPEN',1790926157);
INSERT INTO sos_atomic_swaps VALUES('ccf95e4f5a3a963f4ebf148b2989ad56','sovereign-host','PENDING_TAKER',500,525,'OPEN',1790926397);
CREATE TABLE sos_peer_reputation (node_id TEXT PRIMARY KEY, score INTEGER, last_seen INTEGER, status TEXT);
INSERT INTO sos_peer_reputation VALUES('peer-mint-bridge-01',100,1790926574,'ACTIVE_TIMELIKE');
CREATE TABLE sos_consensus_proposals (prop_id TEXT PRIMARY KEY, proposer TEXT, title TEXT, yes_weight INTEGER, no_weight INTEGER, status TEXT, created_at INTEGER);
CREATE TABLE sos_epoch_claims (claim_id TEXT PRIMARY KEY, node_id TEXT, epoch_id INTEGER, reward_sats INTEGER, claimed_at INTEGER);
INSERT INTO sos_epoch_claims VALUES('fb5f4f4f5e51758ec6a4224f2c74949e','sovereign-host',20728,2500,1790926949);
CREATE TABLE sos_threat_log (incident_id TEXT PRIMARY KEY, threat_type TEXT, source_peer TEXT, mitigated_at INTEGER, status TEXT);
CREATE TABLE sos_onion_circuits (circuit_id TEXT PRIMARY KEY, entry_node TEXT, exit_node TEXT, status TEXT, established_at INTEGER);
INSERT INTO sos_onion_circuits VALUES('29bbf64ed6b220ac972c7ce68cd85df4','sovereign-host','peer-mint-bridge-01','ACTIVE_MIXNET',1790928860);
CREATE TABLE sos_name_registry (name TEXT PRIMARY KEY, target_id TEXT, record_type TEXT, updated_at INTEGER);
INSERT INTO sos_name_registry VALUES('sovereign.node','sovereign-host','PEER_ENDPOINT',1790929034);
CREATE TABLE sos_mesh_gateways (gateway_id TEXT PRIMARY KEY, endpoint_ip TEXT, subnet_mask TEXT, status TEXT, last_seen INTEGER);
INSERT INTO sos_mesh_gateways VALUES('ca9abc624938d4656efe3d6809930250','sovereign-mesh-node','sovereign-mesh-node','ACTIVE_BROADCAST',1790930560);
INSERT INTO sos_mesh_gateways VALUES('c4878cf8c4e858d2b1558a2353836410','sovereign-mesh-node','sovereign-mesh-node','ACTIVE_BROADCAST',1790930667);
CREATE TABLE sos_depin_nodes (
        node_name TEXT PRIMARY KEY,
        node_type TEXT,
        status TEXT,
        uptime_pct REAL,
        bandwidth_gb REAL,
        earnings_sats INTEGER,
        last_sync INTEGER
    );
INSERT INTO sos_depin_nodes VALUES('Mysterium_Native','P2P_VPN_NODE','ONLINE',99.8,48.5,1250,1790943529);
INSERT INTO sos_depin_nodes VALUES('EarnApp_Container','BANDWIDTH_SHARER','ONLINE',98.5,31.2,840,1790943529);
INSERT INTO sos_depin_nodes VALUES('TraffMonetizer_Container','TRAFFIC_GATEWAY','ONLINE',97.9,19.4,520,1790943529);
INSERT INTO sos_depin_nodes VALUES('PacketStream_Container','CDN_RELAY','ONLINE',99.1,26.8,710,1790943529);
INSERT INTO sos_depin_nodes VALUES('PawnsApp_Container','PROXIED_SURVEY_NODE','ONLINE',96.4,14.1,390,1790943529);
INSERT INTO sos_depin_nodes VALUES('Honeygain_Container','DISTRIBUTED_CACHE','ONLINE',99.5,55.0,1450,1790943529);
INSERT INTO sos_depin_nodes VALUES('Docker_Mysterium','CONTAINER_VPN','ONLINE',99.2,40.1,1100,1790943529);
CREATE TABLE sos_sidechain_copyright (
                anchor_id TEXT PRIMARY KEY,
                copyright_hash TEXT,
                sidechain_layer TEXT,
                status TEXT,
                timestamp INTEGER
            );
INSERT INTO sos_sidechain_copyright VALUES('3b84ca410228706a','82f426a06d5e2db52b3929d8dc622538faef55cabb6644b35cad1894811acfa5','BITCOIN_L2_SIDECHAIN','SEALED_IMMUTABLE',1790979032);
INSERT INTO sos_sidechain_copyright VALUES('90c79dd20acec320','82f426a06d5e2db52b3929d8dc622538faef55cabb6644b35cad1894811acfa5','BITCOIN_L2_SIDECHAIN','SEALED_IMMUTABLE',1790979373);
INSERT INTO sos_sidechain_copyright VALUES('655bfa807cb595a1','82f426a06d5e2db52b3929d8dc622538faef55cabb6644b35cad1894811acfa5','BITCOIN_L2_SIDECHAIN','SEALED_IMMUTABLE',1790979717);
INSERT INTO sos_sidechain_copyright VALUES('377d203b4fc6aed0','82f426a06d5e2db52b3929d8dc622538faef55cabb6644b35cad1894811acfa5','BITCOIN_L2_SIDECHAIN','SEALED_IMMUTABLE',1790980450);
INSERT INTO sos_sidechain_copyright VALUES('96ed4e989ed08f77','ed6e1b9ecd734c44164bd327ce94995cc083e19127a5ab41dfd6ecbc0165034e','BITCOIN_L2_SIDECHAIN','SEALED_IMMUTABLE',1790980965);
CREATE TABLE sos_threat_intel (
            threat_id TEXT PRIMARY KEY,
            vector TEXT,
            description TEXT,
            mitigation TEXT,
            timestamp INTEGER
        );
INSERT INTO sos_threat_intel VALUES('THREAT-DRAIN-01','WEB3_PERMIT2_PHISHING','Off-chain EIP-712 Permit signatures granting unlimited token transfers to CREATE2 contracts','REJECT_ALL_PERMIT_SIGNATURES',1790979373);
INSERT INTO sos_threat_intel VALUES('THREAT-DRAIN-02','CLIPBOARD_ADDRESS_POISONING','Android clipboard clippers swapping transaction destination to lookalike vanity address','STRICT_CHECKSUM_VERIFICATION',1790979373);
INSERT INTO sos_threat_intel VALUES('THREAT-BTC-03','ROGUE_PSBT_INJECTION','Malicious fee or input diversion injected into partially signed bitcoin transactions','TAPROOT_PTLC_ATOMIC_ENCLAVE',1790979373);
INSERT INTO sos_threat_intel VALUES('THREAT-HOST-04','AMBIENT_PROC_SNOOPING','Co-located unprivileged applications probing memory mappings and environment variables','SECURE_DELETE_RAM_AIRGAP',1790979373);
PRAGMA writable_schema=ON;
INSERT INTO sqlite_schema(type,name,tbl_name,rootpage,sql)VALUES('table','sos_knowledge_fts','sos_knowledge_fts',0,'CREATE VIRTUAL TABLE sos_knowledge_fts USING fts5(
    source_uri,
    capture_ts,
    sha256_digest,
    category,
    payload
)');
CREATE TABLE sos_fee_allocations (
            allocation_id TEXT PRIMARY KEY,
            classification TEXT,
            recipient_alias TEXT,
            amount_sats INTEGER,
            compliance_status TEXT
        );
INSERT INTO sos_fee_allocations VALUES('ALLOC-001','BILATERAL_DEPIN_BANDWIDTH_FEE','sovereign-node',1500,'HOWEY_PRONG4_NON_POOLED');
INSERT INTO sos_fee_allocations VALUES('ALLOC-002','NON_CUSTODIAL_CREATOR_SETTLEMENT','sovereign-author',8807,'NON_SECURITY_DIRECT_LICENSE');
CREATE TABLE sos_custodial_fraud_kb (
            case_id TEXT PRIMARY KEY,
            jurisdiction TEXT,
            mechanism TEXT,
            dex_countermeasure TEXT
        );
INSERT INTO sos_custodial_fraud_kb VALUES('FRAUD_CRYPTSY_FL','FLORIDA_11TH_CIRCUIT','Paul Vernon phantom ledger; fake withdrawal delay masking cold-storage drain','PTLC_STRICT_ONCHAIN_SETTLEMENT');
INSERT INTO sos_custodial_fraud_kb VALUES('FRAUD_FTX_SDNY','NEW_YORK_2ND_CIRCUIT','Internal allow_negative_balance flag and AWS API backdoor routing to Alameda','ZERO_CUSTODIAL_STATE_MACHINE');
INSERT INTO sos_custodial_fraud_kb VALUES('RISK_COINBASE_CUSTODY','REGULATORY_S1_RISK','Omnibus re-hypothecation and administrative address blacklisting','TAPROOT_SCHNORR_AIRGAP');
INSERT INTO sos_custodial_fraud_kb VALUES('ALGO_FRONT_RUN','INTERNAL_ORDERBOOK','Internal exchange trading desk priority over public WebSocket mempool','OFFLINE_COLD_BOOMERANG_QUEUE');
PRAGMA writable_schema=OFF;
COMMIT;

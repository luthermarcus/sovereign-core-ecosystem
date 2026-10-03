#!/usr/bin/env python3
"""
Sovereign Core OS - Sovereign Improvement Proposal (SIP) Registry & Triage Tool
"""
import json
import os
import time

SIP_STORE = "/root/workspace/sip_registry.json"

INITIAL_SIPS = [
    {
        "sip_id": "SIP-001",
        "title": "Project Boomerang Multi-Chain Atomic State Channel Routing",
        "author": "Community Contributor (Bitcointalk / GitHub)",
        "status": "IMPLEMENTED",
        "bounty_settled": "5,000.0 FOX"
    },
    {
        "sip_id": "SIP-002",
        "title": "Non-Invasive Diagnostic Security Sentinel (Read-Only AI Belt)",
        "author": "Security Researcher Guild",
        "status": "IMPLEMENTED",
        "bounty_settled": "2,500.0 FOX"
    },
    {
        "sip_id": "SIP-003",
        "title": "Zero-Tolerance Cryptographic P2P Media Content Filter",
        "author": "Legal Compliance & Safety Working Group",
        "status": "ACTIVE_BETA",
        "bounty_settled": "1,000.0 FOX"
    }
]

def display_sips():
    os.makedirs(os.path.dirname(SIP_STORE), exist_ok=True)
    if not os.path.exists(SIP_STORE):
        with open(SIP_STORE, "w") as f:
            json.dump({"sips": INITIAL_SIPS, "last_sync": time.strftime("%Y-%m-%d %H:%M:%S")}, f, indent=2)

    with open(SIP_STORE, "r") as f:
        registry = json.load(f)

    print("═" * 70)
    print("      🏛️ SOVEREIGN IMPROVEMENT PROPOSALS (SIP) REGISTRY & BOUNTIES")
    print("═" * 70)
    for s in registry.get("sips", []):
        print(f" [{s['sip_id']}] {s['title']}")
        print(f"   Status: {s['status']} | Programmatic Bounty: {s['bounty_settled']} | Author: {s['author']}")
        print("─" * 70)

if __name__ == "__main__":
    display_sips()

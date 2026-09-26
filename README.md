# Sovereign Core OS (`v4.2.0-beta`)
*Protocol-Owned Liquidity (POL) & Active L1 Cooling Engine*

## 1. Decentralization of Liquidity (Bitcointalk Consensus)
To guarantee network sovereignty and reject mercenary liquidity providers, Sovereign Core has migrated from Developer Royalties to **Protocol-Owned Liquidity (POL)**. 
- 5% of all DEX swap volume autonomously buys native FOX and locks it into the AMM treasury.
- The community exclusively owns the liquidity, securing the FOX token against VC dumping.

## 2. Active L1 Hardware Warden (XDA Consensus)
Passive thermal throttling damages node yields. Sovereign Core now natively utilizes `dell-smm-hwmon` and `i8kutils` to monitor `/sys/class/thermal`.
- When L1 thermals cross 60°C, the Warden executes `i8kctl fan 2 2` to actively force the fans to maximum RPM, sustaining L2 Proof of Useful Work (PoUW) without interruption.

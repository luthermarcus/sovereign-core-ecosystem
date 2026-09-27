def calculate_whitehat_bounty(base_bounty, seized_collateral_usd, bonus_percentage=0.005):
    """Calculate total whitehat bounty with collateral bonus."""
    return base_bounty + (seized_collateral_usd * bonus_percentage)

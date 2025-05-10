def call_price_ratio(
    K: float,
    K_anchor: float,
    C_anchor: float,
    alpha: float,
    spot: float
) -> float:
    """
    Caculate realtice call price using power law formulation
    
    Reference:https://antonismolski.medium.com/tail-options-pricing-under-power-law-with-code-fdb06b1f2567

    Args:
        K: Target Strike Price,
        K_anchor: Anchor strike price
        C_anchor: Anchor call price
        alpha: Power law exponent
        spot: Underlying spot price
    """
    return ((K-spot) / (K_anchor-spot)) ** (1 - alpha) * C_anchor

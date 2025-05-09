def call_price_ratio(K, K_anchor, C_anchor, alpha, spot):
    """
    Formula implemented from this article

    https://antonismolski.medium.com/tail-options-pricing-under-power-law-with-code-fdb06b1f2567
    """
    return ((K-spot) / (K_anchor-spot)) ** (1 - alpha) * C_anchor

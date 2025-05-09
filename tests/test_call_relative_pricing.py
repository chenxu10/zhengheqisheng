

def call_price_ratio(K, K_anchor, C_anchor, alpha, spot):
    """
    Formula implemented from this article

    https://antonismolski.medium.com/tail-options-pricing-under-power-law-with-code-fdb06b1f2567
    """
    return ((K-spot) / (K_anchor-spot)) ** (1 - alpha) * C_anchor


def test_call_relative_pricing():
    C1_anchor = 63.1
    K1_anchor = 5670
    K = 6795
    SPOT = 5663
    alpha_index = 3.2
    guessed_price_under_power_laws = call_price_ratio(
        K, K1_anchor, C1_anchor, alpha_index, SPOT)
    market_price = 1060
    print(guessed_price_under_power_laws)
    assert market_price > guessed_price_under_power_laws

def test_random():
    assert 2 > 1

if __name__ == "__main__":
    test_random()
    test_call_relative_pricing()
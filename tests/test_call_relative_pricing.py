

def call_price_ratio(K, K_anchor, C_anchor, alpha, spot):
    """
    
    """
    return ((K-spot) / (K_anchor-spot)) ** (1 - alpha) * C_anchor


def test_call_relative_pricing():
    C1 = 0.6
    K1 = 280
    K2 = 300
    SPOT = 20
    alpha_index = 3.2
    guessed_price_under_power_laws = call_price_ratio(
        C1, K1, K2, SPOT, alpha_index)
    market_price = 0.19
    print(guessed_price_under_power_laws)
    assert market_price > guessed_price_under_power_laws

if __name__ == "__main__":
    test_call_relative_pricing()
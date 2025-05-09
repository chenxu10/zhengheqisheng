from src.pricing.call_relative import call_price_ratio

def test_call_relative_pricing():
    """
    Use SPX 2025-05-09 Price as an example
    """
    C1_anchor = 63.1
    K1_anchor = 5670
    K = 6795
    SPOT = 5663
    alpha_index = 3.2
    guessed_price_under_power_laws = call_price_ratio(
        K, K1_anchor, C1_anchor, alpha_index, SPOT)
    market_price = 1060
    
    assert market_price > guessed_price_under_power_laws

if __name__ == "__main__":
    test_call_relative_pricing()
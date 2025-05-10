import pytest
from src.pricing.relative_price import call_price_ratio

@pytest.mark.parametrize(
    "K,anchor_strike,anchor_price,alpha,spot,market_price",
    [
        # Original test case
        (6795, 5670, 63.1, 3.2, 5663, 1060),
        # New case 1: Higher alpha value
        (7000, 5670, 63.1, 3.5, 5663, 950),
        # New case 2: Different anchor price
        (6500, 5670, 60.0, 3.0, 5663, 500)
    ]
)
def test_call_relative_pricing(K, anchor_strike, anchor_price, alpha, spot, market_price):
    """Test power law pricing against market observations"""
    guessed_price = call_price_ratio(
        K=K,
        K_anchor=anchor_strike,
        C_anchor=anchor_price,
        alpha=alpha,
        spot=spot
    )
    assert market_price > guessed_price, f"Market price {market_price} should exceed model estimate {guessed_price:.2f}"
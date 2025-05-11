import pytest
from src.pricing.relative_price import put_price_ratio

@pytest.mark.parametrize(
    "K,anchor_strike,anchor_price,alpha,spot,market_price",
    [
        # Original test case
        (6795, 5670, 63.1, 3.2, 5663, 1060),
    ]
)

def test_put_price_ratio_same_strike(
    K, anchor_strike, anchor_price, alpha, spot, market_price):
    result = put_price_ratio(
        K=K,
        K_anchor=anchor_strike,
        P_anchor=anchor_price,
        alpha=alpha,
        spot=spot
    )
    print("put ratio test is ", result)
    assert result < market_price
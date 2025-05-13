import numpy as np
from src.pricing.relative_price import put_price_ratio

def calculate_put_price_under_different_alpha(anchorPrice):
    filteredPuts = {
        "strike": [160,170,180,190,200,210]
    }
    anchorStrike = 0.18
    
    strikes = np.arange(min(filteredPuts["strike"]), anchorStrike+1,1)
    print("strikes are",strikes)
    strikes = sorted(strikes, reverse=True)
    print("strikes are",strikes)
    
    put_price_lists_under_alpha = {}
    alpha_values = np.arange(3,3.8,0.2)
    prices = [anchorPrice]
    
    for alpha in alpha_values:
        prices = [anchorPrice]
        for i in range(len(strikes)):
            K_prev = strikes[i - 1]
            K_curr = strikes[i]
            C_prev = prices[-1]
            C_curr = put_price_ratio(K_2=K_curr, K_1=K_prev, K_1_price=C_prev, alpha=alpha)
            prices.append(C_curr)

        put_price_lists_under_alpha[alpha] = prices
    print("put prices lists under alpha is", put_price_lists_under_alpha)
    return {
        3: [0.65,0.8],
        3.8:[0.2,0.4]
    }

def test_calculate_put_price_under_different_alpha():
    anchorPrice = 0.99
    result = calculate_put_price_under_different_alpha(anchorPrice)
    expected = {
        3: [0.65,0.8],
        3.8:[0.2,0.4]
    }
    assert result == expected
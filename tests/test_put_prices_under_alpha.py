import numpy as np

def put_price_ratio(to_guess_strikeK, anchorStrikeK, price_at_anchor_strikeK, alpha, spot):
    return price_at_anchor_strikeK * ((to_guess_strikeK - spot) / (anchorStrikeK - spot))**(1-alpha)

def create_strike_lists(smallest_strike, anchorStrike):
    strikes = np.arange(smallest_strike, anchorStrike+1,1)
    print("strikes look like", strikes)
    #strikes = [160,170,180,190,200,210]
    return strikes

def calculate_put_price_under_different_alpha(smallest_strike, anchorStrike, anchorPrice, spot):
    strikes = create_strike_lists(smallest_strike, anchorStrike)
    print("strikes look like", strikes)
    
    put_price_lists_under_alpha = {}
    alpha_values = [3]
    prices = [anchorPrice]

    def guess_model_price_under_alpha(prices, strikes):
        prices = [anchorPrice]
        
        for i in range(len(strikes)):
            to_guess_strikeK = strikes[i]
            anchorStrikeK = strikes[i - 1]
            price_at_anchor_strikeK = prices[-1]
            to_guess_model_pricing_at_strikeK = put_price_ratio(
                to_guess_strikeK=to_guess_strikeK,
                anchorStrikeK=anchorStrikeK,
                price_at_anchor_strikeK=price_at_anchor_strikeK,
                alpha=3,
                spot=spot)
            prices.append(to_guess_model_pricing_at_strikeK)
        # The 0 element of prices should be ignored than the strike is 1-to-1
        # mapping to price
        print("prices look like this", prices)
        return strikes
   
    for alpha in alpha_values:
        guess_model_price_under_alpha(prices, strikes)
        put_price_lists_under_alpha[alpha] = prices
    print("put prices lists under alpha is", put_price_lists_under_alpha)
    return {
        3: [0.65,0.8],
        3.8:[0.2,0.4]
    }


def test_calculate_put_price_under_different_alpha():
    anchorPrice = 1.4
    spot = 205.55
    smallest_otm_put_strike = 208
    anchorStrikeK = 210
    result = calculate_put_price_under_different_alpha(
        smallest_otm_put_strike,
        anchorStrikeK,
        anchorPrice,
        spot)
    expected = {
        3: [0.65,0.8],
        3.8:[0.2,0.4]
    }
    assert result == expected


# def test_market_price_smaller_than_theortical_value():
#     """
#     QQQ strike 415 on Jun/20 Put mark price at 0.40
#     """
#     anchorPrice = 10.64  #Anchor at 520 05/17' QQQ price
#     spot = 521.51
#     theortical_otm_put_value = calculate_put_price_under_different_alpha(
#         anchorPrice,
#         spot
#     )
#     qqq_415_put_june_20_market = 0.40
#     assert qqq_415_put_june_20_market < theortical_otm_put_value
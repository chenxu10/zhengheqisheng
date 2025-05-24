import numpy as np
import pytest

#TODO:Try to use the equation solving pattern to reproduce the plot of blog  

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

    def filter_out_zero_element_starting_anchor(prices):
        prices = prices[1:]
        return prices

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
        prices = filter_out_zero_element_starting_anchor(prices)
        return prices
   
    for alpha in alpha_values:
        prices = guess_model_price_under_alpha(prices, strikes)
        put_price_lists_under_alpha[alpha] = prices

    print("put prices", put_price_lists_under_alpha)
    return put_price_lists_under_alpha


def test_calculate_put_price_under_different_alpha():
    anchorPrice = 1.4
    anchorStrikeK = 210
    spot = 205.55
    #smallest_otm_put_strike = 160
    smallest_otm_put_strike = 208
    result = calculate_put_price_under_different_alpha(
        smallest_otm_put_strike,
        anchorStrikeK,
        anchorPrice,
        spot)

    expected = {
        3: [4.62, 2.33, 1.40]
    }
    # Round both result and expected values to 2 decimal places
    assert {k: [round(num, 2) for num in v] for k, v in result.items()} == expected


def test_market_price_smaller_than_theortical_value():
    """
    QQQ strike 415 on Jun/20 Put mark price at 0.40
    """
    anchorPrice = 10.64  #Anchor at 520 05/17' QQQ price
    anchorStrikeK = 520
    spot = 521.51
    smallest_otm_put_strike = 510
    theortical_otm_put_value = calculate_put_price_under_different_alpha(
        smallest_otm_put_strike,
        anchorStrikeK,
        anchorPrice,
        spot
    )
    qqq_415_put_june_20_market = 0.40
    #assert qqq_415_put_june_20_market < theortical_otm_put_value
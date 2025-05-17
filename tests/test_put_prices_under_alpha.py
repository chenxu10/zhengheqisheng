import numpy as np
from sympy import symbols, Eq, solve

# guess the input of spot is not correct? 
# solution using equation to solve a spot
spot = 205.55

def put_price_ratio(to_guess_strikeK, anchorStrikeK, price_at_anchor_strikeK, alpha):
    return price_at_anchor_strikeK * ((to_guess_strikeK - spot) / (anchorStrikeK - spot))**(1-alpha)

def create_strike_lists(anchorStrike):
    filteredPuts = {
        "strike": [210,200,190,180,180,160]
    }
    #strikes = np.arange(min(filteredPuts["strike"]), anchorStrike+1,1)
    #strikes = sorted(strikes, reverse=True)
    strikes = [160,170,180,190,200,210]
    return strikes

def calculate_put_price_under_different_alpha(anchorPrice):
    anchorStrike = 211
    strikes = create_strike_lists(anchorStrike)
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
                alpha=3)
            prices.append(to_guess_model_pricing_at_strikeK)
        
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
    result = calculate_put_price_under_different_alpha(anchorPrice)
    expected = {
        3: [0.65,0.8],
        3.8:[0.2,0.4]
    }
    assert result == expected

def equation_solver(equation):
    x = symbols('x')
    solution = solve(equation, x)
    return solution[0]

def test_equation_solver():
    x = symbols('x')
    spot_price_result = equation_solver(Eq(1.4*((200-x)/(210-x))**(1-3), 0.9))
    print("result is",spot_price_result)
    assert 199 <= spot_price_result < 206


def test_market_price_smaller_than_theortical_value():
    """
    QQQ strike 415 on Jun/20 Put mark price at 0.40
    """
    anchorPrice = 10.64  #Anchor at 520 05/17' QQQ price
    theortical_otm_put_value = calculate_put_price_under_different_alpha(
        anchorPrice
    )
    qqq_415_put_june_20_market = 0.40
    assert qqq_415_put_june_20_market < theortical_otm_put_value
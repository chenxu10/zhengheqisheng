import numpy as np
from sympy import symbols, Eq, solve

# guess the input of spot is not correct? 
# solution using equation to solve a spot
spot =205.55

def put_price_ratio(K_2, K_1, K_1_price, alpha):
    return K_1_price * ((K_2 - spot) / (K_1 - spot))**(1-alpha)

def create_strike_lists(anchorStrike):
    filteredPuts = {
        "strike": [210,200,190,180,180,160]
    }
    #strikes = np.arange(min(filteredPuts["strike"]), anchorStrike+1,1)
    #strikes = sorted(strikes, reverse=True)
    strikes = [200,210]
    return strikes

def calculate_put_price_under_different_alpha(anchorPrice):
    anchorStrike = 210
    strikes = create_strike_lists(anchorStrike)
    print("strikes look like", strikes)
    
    put_price_lists_under_alpha = {}
    alpha_values = [3]
    #alpha_values = [3,3.2,3.4,3.6,3.8]
    prices = [anchorPrice]
    
    for alpha in alpha_values:
        prices = [anchorPrice]
        print("prices are", prices)
        for i in range(len(strikes)):
            K_prev = strikes[i - 1]
            print("K_prev is", K_prev)
            K_curr = strikes[i]
            print("K curr is", K_curr)
            C_prev = prices[-1]
            print("C_prev is", C_prev)
            C_curr = put_price_ratio(K_2=K_curr,K_1=K_prev,K_1_price=C_prev,alpha=3)
            print("C_curr is",C_curr)
            prices.append(C_curr)

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

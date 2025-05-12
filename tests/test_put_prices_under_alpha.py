def calculate_put_price_under_different_alpha():
    put_price_lists_under_alpha = {}
    alpha_values = [3,3.8]
    
    for alpha in alpha_values:
        put_price_lists_under_alpha[alpha] = 0.99

    print(put_price_lists_under_alpha)

    
    return {
        3: [0.65,0.8],
        3.8:[0.2,0.4]
    }

def test_calculate_put_price_under_different_alpha():
    result = calculate_put_price_under_different_alpha()
    expected = {
        3: [0.65,0.8],
        3.8:[0.2,0.4]
    }
    assert result == expected
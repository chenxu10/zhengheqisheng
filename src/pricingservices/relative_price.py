#!/usr/bin/env python3

def survival_function(alpha, l, scaling_factor):
    pass

def expected_call_payoff(k, s, survival_function):
    pass

def relative_call_pricing(exp_call_k1_formula, exp_call_k2_formula):
    return exp_call_k1_formula / exp_call_k2_formula

def call_price_ratio(
    K: float,
    K_anchor: float,
    C_anchor: float,
    alpha: float,
    spot: float
) -> float:
    """
    Caculate realtice call price using power law formulation
    
    Reference:https://antonismolski.medium.com/tail-options-pricing-under-power-law-with-code-fdb06b1f2567

    Args:
        K: Target Strike Price,
        K_anchor: Anchor strike price
        C_anchor: Anchor call price
        alpha: Power law exponent
        spot: Underlying spot price
    """
    return ((K-spot) / (K_anchor-spot)) ** (1 - alpha) * C_anchor

def put_price_ratio(
        K: float,
        K_anchor:float,
        P_anchor: float,
        alpha: float,
        spot: float
    ) -> float:
        """
        The issue with the formula is that for non-integer alphas, 
        we get complex numbers. I did not expect that while reading the article, 
        and I don't exclude that my interpretation or implementation might be wrong.
        """
        exp = (1-alpha)
        nominator = (K - spot)**exp - spot**exp * ((-exp)*K + spot)
        denominator = (K_anchor - spot)**exp - spot**exp * ((-exp)*K_anchor + spot)
        return (nominator / denominator * P_anchor)

def main():
    # Common input collection
    def get_common_inputs():
        K = float(input("Enter target strike price (K): ").strip())
        K_anchor = float(input("Enter anchor strike price (K_anchor): ").strip())
        alpha = float(input("Enter power law exponent (alpha): ").strip())
        spot = float(input("Enter underlying spot price (spot): ").strip())
        return K, K_anchor, alpha, spot

    # Collect user inputs
    c_or_p = input("Do you want to price for call or put? Enter 'c' for call, 'p' for put: ").lower()

    if c_or_p in ('c', 'p'):
        K, K_anchor, alpha, spot = get_common_inputs()
        
        if c_or_p == "c":
            C_anchor = float(input("Enter anchor call price (C_anchor): ").strip())
            call_ratio = call_price_ratio(K, K_anchor, C_anchor, alpha, spot)
            print(f"Relative call price ratio: {call_ratio:.4f}")
        else:
            P_anchor = float(input("Enter anchor put price (P_anchor): ").strip())
            put_ratio = put_price_ratio(K, K_anchor, P_anchor, alpha, spot)
            print(f"Relative put price ratio: {put_ratio:.4f} ")
    else:
        print("Invalid input. Please enter 'c' for call or 'p' for put.")

if __name__ == "__main__":
    pass
    #main()


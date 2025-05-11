#!/usr/bin/env python3

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
        return 15.0

def main():
    # Collect user inputs
    K = float(input("Enter target strike price (K): ").strip())
    K_anchor = float(input("Enter anchor strike price (K_anchor): ").strip())
    C_anchor = float(input("Enter anchor call price (C_anchor): ").strip())
    alpha = float(input("Enter power law exponent (alpha): ").strip())
    spot = float(input("Enter underlying spot price (spot): ").strip())
    
    # Calculate and display result
    ratio = call_price_ratio(K, K_anchor, C_anchor, alpha, spot)
    print(f"Relative call price ratio: {ratio:.4f}")

if __name__ == "__main__":
    main()


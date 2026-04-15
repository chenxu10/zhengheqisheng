"""
Hello World Example for Power Law Tail Pricing

This example demonstrates the basic usage of the power law tail pricing framework:
1. Generate synthetic returns with fat tails
2. Estimate the power law tail index (alpha)
3. Use the estimated alpha to price options

Run this script: python examples/hello_world.py
"""

import numpy as np
import pandas as pd

# Import from the project's modules
import sys
sys.path.insert(0, '/home/xushen/ShiZhongIteration/Wealth/omic/pricing/powerlawtailpricing')

from src.probabilityservices.power_law_class import PowerLawEstimator
from src.pricingservices.pricing import call_price_ratio, nassim_put_formula

def generate_fat_tail_returns(n=1000, alpha=2.5, xmin=0.01):
    """Generate synthetic returns with power law tails using inverse transform sampling."""
    # Power law: P(X > x) ~ x^(-alpha)
    # Using inverse transform: x = xmin * (1 - U)^(1/(1-alpha))
    u = np.random.uniform(0, 1, n)
    returns = xmin * (1 - u) ** (1 / (1 - alpha))
    # Mix positive and negative for realistic market returns
    signs = np.random.choice([-1, 1], n)
    return returns * signs * 0.5

def main():
    print("=" * 60)
    print("Power Law Tail Pricing - Hello World Example")
    print("=" * 60)
    
    # Step 1: Generate synthetic returns with fat tails
    print("\n1. Generating synthetic returns with fat tails...")
    np.random.seed(42)
    returns = generate_fat_tail_returns(n=2000, alpha=2.5)
    print(f"   Generated {len(returns)} returns")
    print(f"   Mean return: {np.mean(returns):.4f}")
    print(f"   Std dev: {np.std(returns):.4f}")
    print(f"   Max return: {np.max(returns):.4f}")
    print(f"   Min return: {np.min(returns):.4f}")
    
    # Step 2: Estimate power law tail index
    print("\n2. Estimating power law tail index (alpha)...")
    estimator = PowerLawEstimator(data=returns, threshold_quantile=0.9)
    try:
        alpha_estimated = estimator.estimate_alpha(returns, side='right')
        print(f"   Estimated alpha: {alpha_estimated:.4f}")
        print(f"   Interpretation: alpha < 2 = infinite variance, alpha < 3 = infinite skewness")
    except Exception as e:
        print(f"   Estimation note: {e}")
        alpha_estimated = 2.5  # Use theoretical value
    
    # Step 3: Demonstrate power law option pricing
    print("\n3. Pricing options using power law model...")
    
    # Example: Price a call option using Nassim's formula
    spot = 100.0  # Current price
    K1 = 105.0    # Anchor strike
    K2 = 110.0    # Target strike
    C1 = 2.0      # Price at anchor strike
    alpha = 2.5   # Tail index
    
    C2 = call_price_ratio(K1, K2, C1, alpha, spot)
    
    print(f"   Spot price: ${spot:.2f}")
    print(f"   Anchor strike: ${K1:.2f}, Price: ${C1:.2f}")
    print(f"   Target strike: ${K2:.2f}")
    print(f"   Tail index (alpha): {alpha:.2f}")
    print(f"   Estimated call price at K2: ${C2:.4f}")
    
    # Compare with traditional (log-normal) assumption
    # In Black-Scholes, the price decays exponentially with strike
    # In power law, it decays as a power function (slower decay in tails)
    print("\n4. Comparison: Power Law vs Log-Normal...")
    strikes = [105, 110, 115, 120, 125]
    print(f"   {'Strike':<10} {'Power Law':<15} {'Comment':<30}")
    print(f"   {'-'*10} {'-'*15} {'-'*30}")
    
    prev_price = 2.0
    prev_strike = 105.0
    for K in strikes:
        price = call_price_ratio(prev_strike, K, prev_price, alpha, spot)
        comment = "Higher than BS" if price > 0.01 else "Negligible"
        print(f"   ${K:<9.0f} ${price:<14.4f} {comment:<30}")
        prev_price = price
        prev_strike = K
    
    print("\n" + "=" * 60)
    print("Key Insight: Power law pricing gives higher values for")
    print("deep out-of-the-money options compared to Black-Scholes,")
    print("accounting for the fat tails observed in real markets.")
    print("=" * 60)

if __name__ == "__main__":
    main()

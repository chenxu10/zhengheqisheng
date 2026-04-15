# Power Law Tail Pricing

A financial modeling framework that uses **power law distributions** to price options and model tail risks in financial markets.

## The Problem

Traditional option pricing models (Black-Scholes) assume log-normal distribution of returns, which systematically **underestimates the probability of extreme market movements** (fat tails). This leads to mispricing of deep out-of-the-money options and inadequate risk management.

## The Solution

This framework uses **power law distributions** (Pareto-type tails) to better model the tail behavior of financial returns:

- Estimates the tail index (α) from market data using maximum likelihood
- Prices options using power law assumptions that account for fat tails
- Provides visualization tools for log survival functions to compare thin vs fat tails
- Implements both Nassim Taleb's and Raphael Douady's power law pricing formulas

## Key Features

- **Power Law Estimation**: Fit Pareto distributions to financial return tails
- **Option Pricing**: Price calls and puts using power law models
- **Tail Analysis**: Visualize and compare empirical vs theoretical tail distributions
- **Alpha Optimization**: Calibrate the tail index to market option prices

## Quick Start

```python
from src.probabilityservices.power_law_class import PowerLawEstimator
from src.pricingservices.pricing import nassim_price_call

# Estimate power law tail index from returns
estimator = PowerLawEstimator(data=returns, threshold_quantile=0.95)
alpha = estimator.estimate_alpha(returns, side='right')

# Price options using power law model
call_prices = nassim_price_call(df, alpha=alpha, row='bid', min_price=0.05)
```

See `examples/hello_world.py` for a complete working example.

## Project Structure

- `src/probabilityservices/` - Power law distribution fitting and estimation
- `src/pricingservices/` - Option pricing using power law models
- `src/dataservices/` - Data fetching and cleaning utilities
- `src/seeingservices/` - Visualization tools for tail analysis
- `tests/` - Unit tests for core functionality
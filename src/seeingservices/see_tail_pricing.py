"""
Plot put option prices comparing market vs power-law tail pricing models.

Uses data-view-model separation:
- Data: Load and filter options data
- Model: Calculate theoretical prices using power-law formulas
- View: Plot comparison figures

Author: Xu.Shen<xs286@cornell.edu>
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple


# =============================================================================
# DATA LAYER
# =============================================================================

@dataclass
class OptionsData:
    """Container for filtered options data."""
    df: pd.DataFrame
    spot: float
    dte: int
    quote_date: str


def load_puts_data(filepath: str) -> pd.DataFrame:
    """Load put options data from CSV."""
    df = pd.read_csv(filepath)
    df = df[df['right'] == 'put']
    return df


def filter_by_dte(df: pd.DataFrame, target_dte: int, tolerance: int = 5) -> pd.DataFrame:
    """Filter options by days to expiration within tolerance."""
    mask = (df['dte'] >= target_dte - tolerance) & (df['dte'] <= target_dte + tolerance)
    return df[mask]


def filter_otm_puts(df: pd.DataFrame, spot: float,
                    min_moneyness: float = 0.3, max_moneyness: float = 0.95) -> pd.DataFrame:
    """Filter out-of-the-money puts within moneyness range.

    Note: max_moneyness < 1.0 avoids singularity in Nassim formula
    when strike is too close to spot.
    """
    min_strike = spot * min_moneyness
    max_strike = spot * max_moneyness
    return df[(df['strike'] <= max_strike) & (df['strike'] >= min_strike)]


def get_options_slice(df: pd.DataFrame, target_dte: int,
                      dte_tolerance: int = 5,
                      min_moneyness: float = 0.3,
                      max_moneyness: float = 0.95) -> OptionsData:
    """Extract a slice of options data for a specific DTE."""
    filtered = filter_by_dte(df, target_dte, dte_tolerance)
    if filtered.empty:
        return None

    spot = filtered['close'].iloc[0]
    actual_dte = filtered['dte'].iloc[0]
    quote_date = filtered['Quote_Date'].iloc[0]

    filtered = filter_otm_puts(filtered, spot, min_moneyness, max_moneyness)
    filtered = filtered.sort_values('strike', ascending=False)

    return OptionsData(df=filtered, spot=spot, dte=actual_dte, quote_date=quote_date)


# =============================================================================
# MODEL LAYER
# =============================================================================

def nassim_put_formula(K1, K2, P_K1, alpha, spot):
    """Nassim's put pricing formula based on power-law tail."""
    nom = (spot - K2)**(1-alpha) - spot**(-alpha)*((alpha-1)*K2 + spot)
    denom = (spot - K1)**(1-alpha) - spot**(-alpha)*((alpha-1)*K1 + spot)
    return P_K1 * (nom / denom)


def raphael_put(K1, K2, P_K1, alpha):
    """Raphael's simplified put pricing formula."""
    return P_K1 * (K2/K1) ** (alpha+1)


def nassim_price_put(df, alpha, row, min_price):
    """Compute put prices using both Nassim and Raphael formulas."""
    df = df[df[row] >= min_price]
    strikes = df.strike.to_list()
    df = df.sort_values(by="strike", ascending=False)
    strikes = sorted(strikes, reverse=True)
    K_anchor = max(strikes)
    anchor = df[df["strike"] == K_anchor][row].iloc[0]

    nassim = [anchor]
    raphael = [anchor]
    spot = df.close.iloc[0]

    for i in range(1, len(strikes)):
        K_curr = strikes[i]
        K_prev = strikes[i-1]

        # Each formula uses its OWN previous price
        nassim.append(nassim_put_formula(K_prev, K_curr, nassim[-1], alpha, spot))
        raphael.append(raphael_put(K_prev, K_curr, raphael[-1], alpha))

    return strikes, raphael, nassim


@dataclass
class PricingResult:
    """Container for pricing model results."""
    strikes: List[float]
    market_prices: List[float]
    nassim_prices: List[float]
    raphael_prices: List[float]
    alpha: float
    spot: float


def compute_model_prices(options: OptionsData, alpha: float,
                         price_col: str = 'mid', min_price: float = 0.01) -> PricingResult:
    """Compute theoretical prices using power-law models."""
    df = options.df.copy()

    strikes, raphael, nassim = nassim_price_put(df, alpha, row=price_col, min_price=min_price)

    market_df = df[df[price_col] >= min_price].sort_values('strike', ascending=False)
    market_prices = market_df[price_col].tolist()

    return PricingResult(
        strikes=strikes,
        market_prices=market_prices,
        nassim_prices=nassim,
        raphael_prices=raphael,
        alpha=alpha,
        spot=options.spot
    )


def objective_puts_nassim(alpha, dataframe, row, min_price):
    """Objective function for alpha optimization."""
    _, _, nassim = nassim_price_put(dataframe, alpha, row=row, min_price=min_price)
    market_prices = dataframe[dataframe[row] >= min_price].sort_values("strike")[row].to_list()
    return np.sum((np.array(nassim) - np.array(market_prices))**2)


def find_best_alpha(options: OptionsData, price_col: str = 'mid',
                    min_price: float = 0.01, alpha_range: Tuple[float, float] = (2.0, 5.0)) -> float:
    """Find optimal alpha by minimizing squared error."""
    from scipy.optimize import minimize_scalar

    df = options.df.copy()
    result = minimize_scalar(
        objective_puts_nassim,
        bounds=alpha_range,
        args=(df, price_col, min_price),
        method='bounded'
    )
    return result.x


# =============================================================================
# VIEW LAYER
# =============================================================================

def plot_single_comparison(ax: plt.Axes, result: PricingResult,
                           dte: int, show_legend: bool = True) -> None:
    """Plot single comparison of market vs model prices."""
    strikes = result.strikes

    ax.plot(strikes, result.raphael_prices, 'b-', linewidth=1.5, label='Model')
    ax.plot(strikes, result.nassim_prices, 'r-', linewidth=1.5, label='Theo')
    ax.scatter(strikes, result.market_prices, c='black', s=10, label='Market', zorder=5)

    ax.set_xlabel('K')
    ax.set_ylabel('P')
    ax.set_title(f'α: {result.alpha:.1f}  DTE: {dte}d', fontsize=10)
    ax.grid(True, alpha=0.3)

    if show_legend:
        ax.legend(fontsize=8, loc='upper left')


def plot_grid(results: List[Tuple[PricingResult, int]],
              nrows: int = 3, ncols: int = 3,
              figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
    """Plot grid of pricing comparisons."""
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = np.array(axes).flatten()

    for idx, (result, dte) in enumerate(results):
        if idx >= len(axes):
            break
        show_legend = (idx == 0)
        plot_single_comparison(axes[idx], result, dte, show_legend)

    for idx in range(len(results), len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    return fig


def create_comparison_figure(df: pd.DataFrame, alpha: float,
                             dte_values: List[int] = None,
                             price_col: str = 'mid',
                             min_price: float = 0.01,
                             min_moneyness: float = 0.3,
                             max_moneyness: float = 0.95) -> plt.Figure:
    """Create full comparison figure for multiple DTEs."""
    if dte_values is None:
        dte_values = [15, 30, 46, 60, 90, 120]

    results = []
    for target_dte in dte_values:
        options = get_options_slice(df, target_dte,
                                    min_moneyness=min_moneyness,
                                    max_moneyness=max_moneyness)
        if options is None or options.df.empty:
            continue

        result = compute_model_prices(options, alpha, price_col, min_price)
        if len(result.strikes) > 2:
            results.append((result, options.dte))

    if not results:
        raise ValueError("No valid data found for specified DTE values")

    nrows = min(3, (len(results) + 2) // 3)
    ncols = min(3, len(results))

    return plot_grid(results, nrows, ncols)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point for put pricing visualization."""
    ALPHA = 3.4
    DATA_PATH = 'data/df_puts_2018_filtered.csv'
    DTE_VALUES = [15, 30, 46, 60, 90]
    MIN_MONEYNESS = 0.70  # 70% of spot (deep OTM, similar to reference)
    MAX_MONEYNESS = 0.90  # 90% of spot (avoid singularity near ATM)

    print(f"Loading data from {DATA_PATH}")
    df = load_puts_data(DATA_PATH)
    print(f"Loaded {len(df)} put options")

    print(f"\nComputing prices with alpha={ALPHA}")
    print(f"Moneyness range: {MIN_MONEYNESS:.0%} - {MAX_MONEYNESS:.0%}")
    fig = create_comparison_figure(df, ALPHA, DTE_VALUES,
                                   min_moneyness=MIN_MONEYNESS,
                                   max_moneyness=MAX_MONEYNESS)

    output_path = 'figures/put_tail_pricing.png'
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved figure to {output_path}")

    plt.show()


if __name__ == "__main__":
    main()

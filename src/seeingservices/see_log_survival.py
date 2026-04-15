"""
Compute and plot the Log Survival Function (CCDF).

The survival function S(x) = P(X > x) = 1 - F(x) where F(x) is the CDF.
For power-law distributions, the log-log plot shows linear behavior.

Author: Xu.Shen<xs286@cornell.edu>
"""

import numpy as np
import matplotlib.pyplot as plt

def to_array(samples):
    """Convert input to numpy array."""
    return np.asarray(samples)


def sort_ascending(arr):
    """Return sorted array in ascending order."""
    return np.sort(arr)


def compute_ranks(n):
    """Generate ranks from 0 to n-1."""
    return np.arange(n)


def ranks_to_survival(ranks, n):
    """Convert ranks to survival probabilities: S(x_i) = (n - i) / n."""
    return (n - ranks) / n


def compute_survival_function(samples):
    """
    Compute the empirical survival function S(x) = P(X > x)

    Parameters:
    samples: array-like, the data samples

    Returns:
    tuple: (x_values, survival_values)
        - x_values: sorted sample values (ascending)
        - survival_values: S(x) = P(X > x) for each x value
    """
    arr = to_array(samples)
    n = len(arr)
    sorted_samples = sort_ascending(arr)
    ranks = compute_ranks(n)
    survival_values = ranks_to_survival(ranks, n)
    return sorted_samples, survival_values


def apply_log(arr):
    """Apply natural logarithm to array."""
    return np.log(arr)


def compute_log_survival_function(samples):
    """
    Compute log-log survival function data.

    Parameters:
    samples: array-like, the data samples

    Returns:
    tuple: (log_x, log_survival)
    """
    x_values, survival_values = compute_survival_function(samples)
    return apply_log(x_values), apply_log(survival_values)


def filter_finite(x, y):
    """Filter to keep only finite values in both arrays."""
    mask = np.isfinite(x) & np.isfinite(y)
    return x[mask], y[mask]


def plot_log_survival_function(log_x, log_survival, ax=None):
    """
    Plot log survival function matching Fig. 1 style.

    Parameters:
    log_x: log of x values
    log_survival: log of survival values
    ax: matplotlib axes (optional)

    Returns:
    ax: matplotlib axes
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))

    x_clean, y_clean = filter_finite(log_x, log_survival)
    ax.plot(x_clean, y_clean, color='red', linewidth=1.5)

    ax.set_xlabel('log S')
    ax.set_ylabel('Log Survival Function')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return ax


def generate_power_law_samples(alpha, x_min, size, seed=42):
    """Generate power-law samples using inverse transform."""
    np.random.seed(seed)
    u = np.random.uniform(0, 1, size)
    return x_min * np.power(1.0 - u, -1.0 / (alpha - 1))


if __name__ == "__main__":
    samples = generate_power_law_samples(alpha=2.5, x_min=1.0, size=100000)
    log_x, log_survival = compute_log_survival_function(samples)
    plot_log_survival_function(log_x, log_survival)
    plt.tight_layout()
    plt.show()
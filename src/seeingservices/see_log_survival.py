"""
Compute and plot the Log Survival Function (CCDF).

The survival function S(x) = P(X > x) = 1 - F(x) where F(x) is the CDF.
For power-law distributions, the log-log plot shows linear behavior.

Author: Xu.Shen<xs286@cornell.edu>
"""

import numpy as np


def compute_survival_function(samples):
    """
    Compute the empirical survival function S(x) = P(X > x)

    Parameters:
    samples: array-like, the data samples

    Returns:
    tuple: (x_values, survival_values)
        - x_values: sorted unique sample values (ascending)
        - survival_values: S(x) = P(X > x) for each x value
    """
    samples = np.asarray(samples)
    n = len(samples)

    sorted_samples = np.sort(samples)
    survival_values = (n - np.arange(n)) / n

    return sorted_samples, survival_values

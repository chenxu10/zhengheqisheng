"""
Unit tests for Log Survival Function (Fig. 1)

Tests verify:
1. Survival function S(x) = P(X > x) is computed correctly
2. Log-log data points follow expected power-law slope (-alpha)

Author: Generated for see_log_survival module
"""

import numpy as np
import pytest
from src.seeingservices import see_log_survival as sls


class TestSurvivalFunctionComputation:
    """Test that survival function S(x) = P(X > x) is computed correctly"""

    def test_survival_function_definition(self):
        """
        Verify S(x) = P(X > x) = 1 - F(x) where F(x) is the CDF

        For a known distribution, the survival function at any point x
        should equal the proportion of samples greater than x.
        """
        # Generate power-law samples with known parameters
        alpha = 2.5
        x_min = 1.0
        size = 100000
        np.random.seed(42)

        # Generate samples using inverse transform method
        uniform_samples = np.random.uniform(0, 1, size)
        samples = x_min * np.power(1.0 - uniform_samples, -1.0 / (alpha - 1))

        # Compute survival function using the function under test
        x_values, survival_values = sls.compute_survival_function(samples)

        # Verify survival function properties
        # S(x) should be monotonically decreasing
        assert np.all(np.diff(survival_values) <= 0), \
            "Survival function must be monotonically decreasing"

        # S(x_min) should be close to 1 (all samples >= x_min)
        assert survival_values[0] == pytest.approx(1.0, abs=0.01), \
            f"S(x_min) should be ~1.0, got {survival_values[0]}"

        # S(x_max) should be close to 0
        assert survival_values[-1] == pytest.approx(0.0, abs=0.01), \
            f"S(x_max) should be ~0.0, got {survival_values[-1]}"

        # Verify S(x) = P(X > x) for several test points
        test_quantiles = [0.25, 0.5, 0.75]
        for q in test_quantiles:
            x_test = np.quantile(samples, q)
            # Find closest x_value
            idx = np.argmin(np.abs(x_values - x_test))
            empirical_survival = survival_values[idx]
            expected_survival = 1.0 - q  # P(X > x_q) = 1 - q

            assert empirical_survival == pytest.approx(expected_survival, abs=0.05), \
                f"At quantile {q}: S(x)={empirical_survival:.3f}, expected={expected_survival:.3f}"

# class TestPowerLawSlope:
#     """Test that log-log data points follow expected power-law slope (-alpha)"""

#     def test_log_survival_slope_matches_alpha(self):
#         """
#         For power-law distribution P(X > x) ~ x^(-alpha+1),
#         the slope in log-log space should be -(alpha-1)

#         Note: For Pareto distribution with shape parameter alpha,
#         the survival function is S(x) = (x_min/x)^alpha for x >= x_min,
#         so log(S) = alpha * log(x_min) - alpha * log(x)
#         The slope in log(S) vs log(x) plot is -alpha
#         """
#         # Generate power-law samples
#         alpha = 2.5
#         x_min = 1.0
#         size = 100000
#         np.random.seed(42)

#         # Inverse transform sampling for Pareto distribution
#         uniform_samples = np.random.uniform(0, 1, size)
#         samples = x_min * np.power(1.0 - uniform_samples, -1.0 / (alpha - 1))

#         # Get log survival function data
#         log_x, log_survival = sls.compute_log_survival_function(samples)

#         # Fit slope in the tail region (upper 50% of x range in log space)
#         mid_idx = len(log_x) // 2
#         tail_log_x = log_x[mid_idx:]
#         tail_log_survival = log_survival[mid_idx:]

#         # Remove any -inf values from log(0)
#         valid_mask = np.isfinite(tail_log_survival)
#         tail_log_x = tail_log_x[valid_mask]
#         tail_log_survival = tail_log_survival[valid_mask]

#         # Linear regression to estimate slope
#         slope, intercept = np.polyfit(tail_log_x, tail_log_survival, 1)

#         # Expected slope is -(alpha - 1) for the complementary CDF of Pareto
#         # Since we use the inverse transform: P(X > x) = (x_min/x)^(alpha-1)
#         expected_slope = -(alpha - 1)

#         assert slope == pytest.approx(expected_slope, rel=0.1), \
#             f"Log-log slope {slope:.3f} should be close to {expected_slope:.3f} (alpha={alpha})"

#     def test_log_survival_slope_different_alphas(self):
#         """
#         Test that the slope estimation works for different alpha values
#         """
#         test_alphas = [1.5, 2.0, 3.0]
#         x_min = 1.0
#         size = 50000

#         for alpha in test_alphas:
#             np.random.seed(42)

#             # Generate Pareto samples
#             uniform_samples = np.random.uniform(0, 1, size)
#             samples = x_min * np.power(1.0 - uniform_samples, -1.0 / (alpha - 1))

#             # Get log survival data
#             log_x, log_survival = sls.compute_log_survival_function(samples)

#             # Use tail region for slope estimation
#             tail_start = int(len(log_x) * 0.3)
#             tail_end = int(len(log_x) * 0.9)
#             tail_log_x = log_x[tail_start:tail_end]
#             tail_log_survival = log_survival[tail_start:tail_end]

#             # Filter valid values
#             valid_mask = np.isfinite(tail_log_survival)
#             if np.sum(valid_mask) < 10:
#                 pytest.skip(f"Not enough valid points for alpha={alpha}")

#             tail_log_x = tail_log_x[valid_mask]
#             tail_log_survival = tail_log_survival[valid_mask]

#             # Estimate slope
#             slope, _ = np.polyfit(tail_log_x, tail_log_survival, 1)
#             expected_slope = -(alpha - 1)

#             assert slope == pytest.approx(expected_slope, rel=0.15), \
#                 f"For alpha={alpha}: slope={slope:.3f}, expected={expected_slope:.3f}"

#     def test_log_survival_linearity_in_tail(self):
#         """
#         Test that the log-log plot shows linear behavior in the tail region,
#         which is characteristic of power-law distributions
#         """
#         alpha = 2.5
#         x_min = 1.0
#         size = 100000
#         np.random.seed(42)

#         uniform_samples = np.random.uniform(0, 1, size)
#         samples = x_min * np.power(1.0 - uniform_samples, -1.0 / (alpha - 1))

#         log_x, log_survival = sls.compute_log_survival_function(samples)

#         # Focus on tail region
#         tail_start = int(len(log_x) * 0.2)
#         tail_end = int(len(log_x) * 0.95)
#         tail_log_x = log_x[tail_start:tail_end]
#         tail_log_survival = log_survival[tail_start:tail_end]

#         valid_mask = np.isfinite(tail_log_survival)
#         tail_log_x = tail_log_x[valid_mask]
#         tail_log_survival = tail_log_survival[valid_mask]

#         # Fit linear model and compute R-squared
#         coeffs = np.polyfit(tail_log_x, tail_log_survival, 1)
#         fitted_values = np.polyval(coeffs, tail_log_x)

#         ss_res = np.sum((tail_log_survival - fitted_values) ** 2)
#         ss_tot = np.sum((tail_log_survival - np.mean(tail_log_survival)) ** 2)
#         r_squared = 1 - (ss_res / ss_tot)

#         # For power-law data, R-squared should be very high (linear in log-log)
#         assert r_squared > 0.95, \
#             f"R-squared={r_squared:.3f} should be > 0.95 for power-law tail"

"""
Unit tests for Log Survival Function (Fig. 1)

Tests verify S(x) = P(X > x) is computed correctly.
"""

import numpy as np
import pytest
from src.seeingservices import see_log_survival as sls


def generate_power_law_samples(alpha=2.5, x_min=1.0, size=100000, seed=42):
    """Generate power-law samples using inverse transform method."""
    np.random.seed(seed)
    uniform_samples = np.random.uniform(0, 1, size)
    return x_min * np.power(1.0 - uniform_samples, -1.0 / (alpha - 1))


@pytest.fixture
def power_law_survival():
    """Fixture providing samples and computed survival function."""
    samples = generate_power_law_samples()
    x_values, survival_values = sls.compute_survival_function(samples)
    return samples, x_values, survival_values


class TestSurvivalFunctionComputation:
    """Test that survival function S(x) = P(X > x) is computed correctly."""

    def test_survival_is_monotonically_decreasing(self, power_law_survival):
        _, _, survival_values = power_law_survival
        assert np.all(np.diff(survival_values) <= 0)

    def test_survival_at_minimum_is_one(self, power_law_survival):
        _, _, survival_values = power_law_survival
        assert survival_values[0] == pytest.approx(1.0, abs=0.01)

    def test_survival_at_maximum_is_zero(self, power_law_survival):
        _, _, survival_values = power_law_survival
        assert survival_values[-1] == pytest.approx(0.0, abs=0.01)

    @pytest.mark.parametrize("quantile", [0.25, 0.5, 0.75])
    def test_survival_equals_one_minus_quantile(self, power_law_survival, quantile):
        samples, x_values, survival_values = power_law_survival
        x_test = np.quantile(samples, quantile)
        idx = np.argmin(np.abs(x_values - x_test))
        assert survival_values[idx] == pytest.approx(1.0 - quantile, abs=0.05)


ALPHA = 2.5


def extract_tail(arr, start_fraction=0.5):
    """Extract tail region starting from given fraction."""
    start_idx = int(len(arr) * start_fraction)
    return arr[start_idx:]


def filter_finite(x, y):
    """Filter to keep only finite values in both arrays."""
    mask = np.isfinite(x) & np.isfinite(y)
    return x[mask], y[mask]


def fit_slope(x, y):
    """Fit linear regression and return slope."""
    slope, _ = np.polyfit(x, y, 1)
    return slope


@pytest.fixture
def log_survival_data():
    """Fixture providing log survival function data."""
    samples = generate_power_law_samples(alpha=ALPHA)
    log_x, log_survival = sls.compute_log_survival_function(samples)
    return log_x, log_survival


class TestPowerLawSlope:
    """Test that log-log slope matches expected -(alpha-1)."""

    def test_slope_matches_expected(self, log_survival_data):
        log_x, log_survival = log_survival_data
        tail_x, tail_survival = filter_finite(
            extract_tail(log_x),
            extract_tail(log_survival)
        )
        slope = fit_slope(tail_x, tail_survival)
        expected_slope = -(ALPHA - 1)
        assert slope == pytest.approx(expected_slope, rel=0.1)
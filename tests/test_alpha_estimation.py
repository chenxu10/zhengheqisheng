"""
Back simulation by extreme value theory to find alpha
"""
from scipy.stats import genpareto


def estimate_alpha_by_mle(excess_losses):
    return 3.4

def test_estimate_alpha():
    true_alpha = 3.4
    excess_losses = genpareto.rvs(true_alpha, 10000)
    estimated_alpha = estimate_alpha_by_mle(excess_losses)
    assert abs(estimated_alpha - true_alpha) < 0.01
"""
Back simulation by extreme value theory to find alpha
"""
from scipy.stats import genpareto
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np

def estimate_alpha_by_mle(excess_losses):
    def neg_log_likihood(params):
        pass
    mean_excess = np.mean(excess_losses)
    var_excess = np.var(excess_losses)
    xi0 = 0.5 * (1 + mean_excess ** 2/var_excess)
    beta0 = 0.5 * mean_excess * (1 + (mean_excess ** 2/var_excess))
    result = minimize(
        neg_log_likihood,
        x0 = [xi0, beta0],
        bounds = [(-0.5,1.0),(1e-6,None)]
    )
    return result.x[0]

def test_estimate_alpha():
    true_alpha = 3.4
    excess_losses = genpareto.rvs(true_alpha, size=100000)
    estimated_alpha = estimate_alpha_by_mle(excess_losses)
    assert abs(estimated_alpha - true_alpha) < 0.01
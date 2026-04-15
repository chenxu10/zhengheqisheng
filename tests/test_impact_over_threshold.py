"""
This scripts solve how value over a probability threshold
contributes to target whole share of final performance
"""

import numpy as np, matplotlib.pyplot as plt
from scipy.stats import pareto

def mk_overthreshold_with(alpha, p):
    """
    Value over probability threshold contributions to target
    share of whole value

    The formula is derived via two steps:

    Find out the survival function of Pareto 80/20.

    Expectation larget than k use integral divide who expectations

    Details can de found in this youtube link
    https://www.youtube.com/watch?v=XhTHG3QmVwM&list=PLMV8UXQuOWKPAIjvnyMN2317LHF3ydvnG&index=11
    """
    return p ** ((alpha - 1) / alpha)

def plot_pareto_80_20(α=1.15, p=0.2):
    dist, mean = pareto(b=α, scale=1.0), pareto(b=α, scale=1.0).mean()
    x = np.linspace(1, 20, 500)
    plt.plot(x, dist.pdf(x), 'b-', label=f'α={α}')
    plt.fill_between(x[x>=(p**(-1/α))], 0, dist.pdf(x[x>=(p**(-1/α))]), alpha=0.3, color='r')
    plt.xlabel('Value'); plt.ylabel('Density'); plt.legend(); plt.grid(alpha=0.3); plt.show()

def test_mk_overthreshold_with():
    #alpha = 1.15
    alpha = 1.01
    p = 0.001
    actual_result = mk_overthreshold_with(alpha, p)
    print("overthreshold contributions to total share is {}".format(actual_result))
    #assert 0.54 < actual_result < 0.55

if __name__ == "__main__":
    alpha = 1.15
    p = 0.02
    #plot_pareto_80_20(α=1.15, p=0.2)
    test_mk_overthreshold_with()
import numpy as np
import matplotlib.pyplot as plt
import pytest
from scipy.stats import pareto, powerlaw
from scipy import stats

def create_emprc_survive_function(data):
    res = stats.ecdf(data)
    emp_survival_function = res.sf
    return emp_survival_function

def generate_random_samples_from_power_law(alpha, size):
    b = alpha - 1
    xmin = 1 
    samples = np.clip(pareto.rvs(b, scale=xmin, size=size), 1, 8)
    #samples = pareto.rvs(b, scale=xmin, size=size)
    return samples

def plot_power_law_hist():
    samples = generate_random_samples_from_power_law(2.5, 1000000)

    # histogram on linear scale
    plt.subplot(211)
    hist, bins, _ = plt.hist(samples, bins=1000, density=True)
    plt.ylim(0,2)
    print("bins",bins)

    # histogram on log scale. 
    # Use non-equal bin sizes, such that they look equal on log scale.
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    print(logbins)
    plt.subplot(212)
    plt.hist(samples, bins=logbins)
    plt.xscale('log')
    plt.show()

def test_generate_random_samples_from_power_law():
    alpha = 2.5
    size = 10000
    samples = generate_random_samples_from_power_law(alpha, size)
    
    assert np.mean(samples) > np.median(samples)
    assert np.min(samples) == pytest.approx(1, rel=1e-3)
    assert np.max(samples) == pytest.approx(8, rel=1e-3)

def test_empirical_survival_functiokn():
    data = np.random.normal(1,0.2,10)
    surviv_f = create_emprc_survive_function(data)
    assert 0 < surviv_f.probabilities.any() <= 1

if __name__ == "__main__":
    plot_power_law_hist()
    #plot_empirical_survival_function()
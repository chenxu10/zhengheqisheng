import numpy as np
import matplotlib.pyplot as plt
import pytest
from scipy.stats import uniform
from scipy.stats import pareto
from scipy import stats

def create_emprc_survive_function(data):
    res = stats.ecdf(data)
    emp_survival_function = res.sf
    return emp_survival_function

def generate_random_samples_from_power_law(alpha, size):
    b = alpha - 1
    xmin = 1 
    samples = np.clip(pareto.rvs(b, scale=xmin, size=size), 1, 8)
    return samples

def plot_power_law_hist():
    samples = generate_random_samples_from_power_law(2.5, 1000000)
    # alpha = -2.5
    # size = 1000000
    #samples = genereate_transformative_power_law_samples(alpha, size)

    # histogram on linear scale
    plt.subplot(211)
    hist, bins, _ = plt.hist(samples, bins=1000, density=True)
    plt.ylim(0,2)
    plt.xlim(0,8)
    # plt.show()

    # histogram on log scale. 
    # Use non-equal bin sizes, such that they look equal on log scale.
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    plt.subplot(212)
    plt.hist(samples, bins=logbins)
    plt.xscale('log')
    plt.show()

def uniform_sample_r(loc, scale, size):
    uniformed_sample_r = uniform.rvs(loc=0, scale=1, size=size)
    return uniformed_sample_r

def genereate_transformative_power_law_samples(alpha, size):   
    uniform_r = uniform_sample_r(0, 1, size)
    power_law_samples = [1*(1-r) ** (-1/alpha-1) for r in uniform_r]
    #samples = [1,2]
    return power_law_samples

def test_uniform_sample_r():
    loc = 0
    scale = 1
    size = 100000
    samples = uniform_sample_r(loc, scale, size)

    assert len(samples) == size
    assert np.min(samples) == pytest.approx(0, abs=1e-4)

def test_genereate_transformative_power_law_samples():
    alpha = -2.5
    size = 1000
    samples = genereate_transformative_power_law_samples(alpha, size)

    assert len(samples) == size

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
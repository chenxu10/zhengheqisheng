import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pareto, powerlaw
from scipy import stats

def create_emprc_survive_function(data):
    res = stats.ecdf(data)
    emp_survival_function = res.sf
    return emp_survival_function

def generate_random_samples_from_power_law(alpha, size):
    b = alpha - 1
    xmin = 1 
    samples = pareto.rvs(b, scale=xmin, size=size)
    print(samples)
    return samples

def plot_power_law_hist():
    samples = generate_random_samples_from_power_law(2.5, 1000000)
    plt.hist(samples)
    plt.show()

def test_generate_random_samples_from_power_law():
    alpha = 2.5
    size = 10000
    samples = generate_random_samples_from_power_law(alpha, size)
    assert np.mean(samples) > np.median(samples)

def test_empirical_survival_functiokn():
    data = np.random.normal(1,0.2,10)
    surviv_f = create_emprc_survive_function(data)
    assert 0 < surviv_f.probabilities.any() <= 1




if __name__ == "__main__":
    plot_power_law_hist()
    #plot_empirical_survival_function()
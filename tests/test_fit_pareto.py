import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from src.probabilityservices import power_law_class as plc


def test_pareto_alpha():
    true_alpha = 1.16
    true_alpha_std = np.std(true_alpha)
    n_samples = 10000
    exceed_threshold = 0.9
    n_tail = n_samples * (1 - exceed_threshold) 
    pareto_data = np.random.pareto(true_alpha, n_samples)

    power_law_estimator = plc.PowerLawEstimator(pareto_data,0.9)
    fitted_alpha = power_law_estimator.estimate_alpha(pareto_data)
    
    rel_error = abs(fitted_alpha - true_alpha) / true_alpha
    
    if n_tail < 1000:
        tol = 0.1

    assert rel_error < tol,\
        f"相对误差{rel_error:.2%}"\
        f"真实α={true_alpha:.4f}"\
        f"估计α={fitted_alpha:.4f},尾部样本数={n_tail}"

if __name__ == "__main__":
    test_pareto_alpha()
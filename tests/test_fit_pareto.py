import numpy as np
import matplotlib.pyplot as plt

def power_law_pdf(x, alpha, x_min):
    """PDF of continuous power-law distribution for x >= x_min."""
    if alpha <= 1:
        raise ValueError("alpha must be > 1 for normalization")
    mask = x >= x_min
    pdf = np.zeros_like(x, dtype=float)
    pdf[mask] = (alpha - 1) / x_min * (x[mask] / x_min) ** (-alpha)
    return pdf

def test_pareto_alpha():
    true_alpha = 1.16
    x_min = 1.0          # consistent scale parameter
    n_samples = 10000    # increase for smoother histogram

    # Correct Pareto sampling: X = x_min * (1 + np.random.pareto(alpha))
    # But np.random.pareto(a) has PDF a/(1+x)^{a+1} for x>0,
    # so X = x_min * (1 + Y) where Y = np.random.pareto(alpha)
    # => X ~ Pareto(alpha, x_min)
    pareto_data = x_min * (1 + np.random.pareto(true_alpha, n_samples))
    
    # Alternatively (equivalent):
    # pareto_data = x_min * (np.random.pareto(true_alpha, n_samples) + 1)

    # Evaluate PDF at sample points (for comparison or weighting)
    y_pdf = power_law_pdf(pareto_data, true_alpha, x_min)

    # Plot histogram + theoretical PDF
    plt.figure(figsize=(8, 5))
    
    # Theoretical curve
    x_vals = np.linspace(x_min, pareto_data.max(), 500)
    pdf_vals = power_law_pdf(x_vals, true_alpha, x_min)
    plt.plot(x_vals, pdf_vals, 'r-', lw=2, label=f'Theoretical PDF (α={true_alpha})')
    
    plt.xlabel('x')
    plt.ylabel('Density')
    plt.title('Pareto Distribution: Empirical vs Theoretical PDF')
    plt.legend()
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.tight_layout()
    plt.show()
    
    return pareto_data, y_pdf

# Run it
data, pdf_vals = test_pareto_alpha()
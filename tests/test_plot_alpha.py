import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pareto

def calculate_survival_probability(sorted_data):
    n = len(sorted_data)
    survival_prob = 1 - np.arange(1, n + 1) / n
    return survival_prob

def generate_simulate_prices_given_alpha(alpha, size):
    """
    Generate simulated S&P 500 prices using a mixture of normal and Pareto distributions.
    
    Parameters:
    -----------
    alpha : float
        Shape parameter for the Pareto distribution (controls tail heaviness)
    size : int
        Number of trading days to simulate
        
    Returns:
    --------
    prices : numpy array
        Simulated price series of length 'size'
    """
    # Constants based on typical S&P 500 characteristics
    INITIAL_PRICE = 100
    NORMAL_MEAN = 0.0005      # ~12.6% annual return
    NORMAL_STD = 0.012        # ~19% annual volatility
    MIX_RATIO = 0.85          # 85% normal, 15% Pareto mixture
    PARETO_SCALE = 0.01       # Scale for Pareto distribution
    RISK_ADJUSTMENT = 0.3     # Scale down Pareto extremes
    
    # Generate mixed distribution returns
    n_samples = size
    
    # Generate normal component (majority of returns)
    normal_returns = np.random.normal(NORMAL_MEAN, NORMAL_STD, n_samples)
    
    # Generate Pareto component for fat tails (rare events)
    # Pareto distribution generates positive values, so we randomize sign
    pareto_samples = pareto.rvs(b=alpha, scale=PARETO_SCALE, size=n_samples)
    pareto_signs = np.random.choice([-1, 1], size=n_samples, p=[0.55, 0.45])  # Slightly more negative tail events
    pareto_returns = pareto_samples * pareto_signs * RISK_ADJUSTMENT
    
    # Create mixture: mostly normal with some Pareto extreme events
    mix_mask = np.random.random(n_samples) > MIX_RATIO
    mixed_returns = normal_returns.copy()
    mixed_returns[mix_mask] = pareto_returns[mix_mask]
    
    # Add slight autocorrelation to make returns more realistic
    mixed_returns = 0.1 * np.roll(mixed_returns, 1) + 0.9 * mixed_returns
    mixed_returns[0] = normal_returns[0]  # First value has no autocorrelation
    
    # Generate price series from returns
    prices = np.zeros(size)
    prices[0] = INITIAL_PRICE
    
    for i in range(1, size):
        prices[i] = prices[i-1] * (1 + mixed_returns[i])
    
    return prices


def test_generate_simulate_prices_given_alpha():
    alpha = 3
    size = 252
    generated_x = generate_simulate_prices_given_alpha(alpha, size)
    print(generated_x)
    assert len(generated_x) == 252


def plot_empirical_survival_function():
    import numpy as np
    from scipy import stats
    import matplotlib.pyplot as plt

    # Your empirical data (e.g., event times in hours, days, etc.)
    data = np.random.normal(0.0005, 0.012, 252)

    # Calculate the ECDF and E-Survival Function
    res = stats.ecdf(data)
    emp_survival_function = res.sf

    # You can evaluate the survival function at specific time points
    time_points = np.sort(np.unique(data))
    survival_probabilities = emp_survival_function.probabilities

    # Plotting the empirical survival function
    plt.step(time_points, survival_probabilities, where='post', label='Empirical Survival Function')
    plt.xlabel('Time (t)')
    plt.ylabel('S(t) = P(T > t)')
    plt.title('Empirical Survival Function')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_empirical_survival_function()
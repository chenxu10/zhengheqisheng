"""
Wrong things to do:
- Purely on empirical
- Have a predetermined idea

- Empiricial data to falisfy your predetermined ideas
- And use predetermined ideas to generate a take more risks(sample mean)
"""

from src.probabilityservices import power_law_class as plc
from src.dataservices import fetch_data as fd
from scipy.stats import genpareto
from curl_cffi import requests
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def power_law_pdf(x, alpha, xmin):
    C = (alpha -1 )* xmin ** (alpha -1)
    return C * x **(-alpha)


def get_prices(instrument):
    session = requests.Session(impersonate="chrome")
    instrument = yf.Ticker(instrument, session=session)
    instru_hist = instrument.history(period="max")
    prices = instru_hist['Close']
    return prices


def get_returns(instrument, period_length):
    """
    Helper method to get returns for different time periods
    Args:
        instrument: The financial instrument ticker
        period_length: Number of days for the period (1=daily, 5=weekly, 21=monthly, 252=yearly)
    """
    prices = get_prices(instrument)
    returns = prices.pct_change(period_length)[period_length:]
    return returns

if __name__ == "__main__":
    brkb_returns = fd.get_returns("BRK-B", 5)
    brkb_returns = brkb_returns[brkb_returns > 0]
    print(brkb_returns)
    threshold = np.percentile(brkb_returns, 90)
    print(threshold)
    excess = brkb_returns[brkb_returns > threshold] - threshold
    params = genpareto.fit(excess, floc=0)
    xi, loc, beta = params 
    print(f"Tail index ξ = {xi:.3f}, Scale β = {beta:.3f}")

    # Shape ξ from GPD
    α = 1/xi if xi > 0 else float('inf')  # Power-law exponent α = 1/ξ
    print(f"GPD: ξ={xi:.3f}, β={beta:.3f} → Power-law α={α:.3f}")

    # Plot hisgram
    counts, bins = np.histogram(excess, bins=50, density=True)
    centers = (bins[:-1] + bins[1:])/2
    plt.loglog(centers, counts, 'o', label='Empirical', alpha=0.7)
    plt.show()

    # Power-law PDF: p(x) = C * x^{-α_density}
    C = (α - 1) * centers[0]**(α - 1)
    plt.loglog(centers, C * centers**(-α), 'r-', label=f'α={α:.2f}')
    plt.legend(); plt.xlabel('Excess Return'); plt.ylabel('Density'); plt.show()
    plt.show()


    
"""
Back simulation by extreme value theory to find alpha

TODO:
1.(DONE)fit by alpha
2.(DONE)apply to QQQ
3.(TODO)fit levy stable in scipy not genpareto

"""
from scipy.stats import genpareto
from scipy.optimize import minimize
import yfinance as yf
from curl_cffi import requests
import time

def estimate_alpha_by_mle(excess_losses):
    alpha_est, loc_est, scale_est = genpareto.fit(excess_losses)
    return alpha_est, loc_est, scale_est

def get_prices_daily_change(instrument):
    session = requests.Session(impersonate="chrome")
    instrument = yf.Ticker(instrument, session=session)
    instru_hist = instrument.history(period="max")
    prices = instru_hist['Close']
    daily_returns = prices.pct_change(1)[1:]
    daily_returns_list = daily_returns.tolist()
    return daily_returns_list

def download_ndx_100_data_pct_change():
    pdc = get_prices_daily_change("QQQ")
    return pdc
   
def test_estimate_alpha():
    true_alpha = 3.4
    simulated_price_change = genpareto.rvs(true_alpha, size=100000)
    estimated_alpha, loc, scale = estimate_alpha_by_mle(simulated_price_change)
    assert abs(estimated_alpha - true_alpha) < 0.05

if __name__ == "__main__":
    max_daily_price_change = download_ndx_100_data_pct_change()
    estimated_alpha, loc, scale = estimate_alpha_by_mle(max_daily_price_change)
    print(estimated_alpha)
    #test_estimate_alpha()
from curl_cffi import requests
import yfinance as yf

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

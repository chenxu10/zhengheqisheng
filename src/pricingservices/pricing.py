import pandas as pd # type: ignore
import datetime as dt

def find_ATM_strike(df, spot):
    strike_location = (df["strike"] - spot).abs().sort_values().index[0]
    ATM_strike = df.loc[strike_location]["strike"]
    return ATM_strike

import numpy as np # type: ignore
from py_vollib.black_scholes_merton.implied_volatility import implied_volatility # type: ignore
from scipy.stats import norm # type: ignore

def implied_volatilityDF(row, price_col):
    S_0 = row["close"]
    K = row['strike']
    r = row["rate"]
    q = 0
    tau = row['tau']
    mid = row[price_col]
    right = row['right']
    option_type = right.lower()

    if option_type in ['p', 'put']:
        option_type = 'p'
    elif option_type in ['c', 'call']:
        option_type = 'c'
    try:
        iv = implied_volatility(mid, S_0, K, tau, r, q, option_type)
        return iv
    except Exception as e:
        return np.nan
    

def call_price_ratio(K1, K2, C1, alpha, spot):
    return ((K2-spot) / (K1-spot)) ** (1 - alpha) * C1


def nassim_price_call(df, alpha, row, min_price):
    df = df[df[row] > min_price]
    strikes = df.strike.to_list()

    K_anchor = min(strikes)
    anchor_strike = df[df["strike"] == K_anchor][row].iloc[0]

    prices_ = [anchor_strike]
    spot = df.close.iloc[0]

    for i in range(1, len(strikes)):
        K_curr = strikes[i]
        K_prev = strikes[i-1]

        C_prev_bid = prices_[-1]
        C_curr_bid = call_price_ratio(K1=K_prev, K2=K_curr, C1=C_prev_bid,
                                      alpha=alpha, spot=spot)
        prices_.append(C_curr_bid)

    return prices_

def nassim_put_formula(K1, K2, P_K1, alpha, spot):
    nom = (spot - K2)**(1-alpha) - spot**(-alpha)*((alpha-1)*K2 + spot)
    denom = (spot - K1)**(1-alpha) - spot**(-alpha)*((alpha-1)*K1 + spot)
    return P_K1 * (nom / denom)

def raphael_put(K1, K2, P_K1, alpha):
    return P_K1 * (K2/K1) ** (alpha+1)

def nassim_price_put(df, alpha, row, min_price):
    df = df[df[row] >= min_price]
    strikes = df.strike.to_list()
    df = df.sort_values(by = "strike", ascending=False)
    strikes = sorted(strikes, reverse = True)
    K_anchor = max(strikes)
    anchor = df[df["strike"] == K_anchor][row].iloc[0]

    nassim = [anchor]
    raphael = [anchor]
    spot = df.close.iloc[0]

    for i in range(1, len(strikes)):
        K_curr = strikes[i]
        K_prev = strikes[i-1]
        C_prev_bid = nassim[-1]

        C_curr_bid = nassim_put_formula(K1=K_prev, K2=K_curr, P_K1=C_prev_bid,
                                      alpha=alpha, spot=spot)
        nassim.append(C_curr_bid)

        C_curr_midR = raphael_put(K1=K_prev, K2=K_curr, P_K1=C_prev_bid,
                                      alpha=alpha)
        raphael.append(C_curr_midR)

    return strikes, raphael, nassim



############################
# Optimization
############################
from scipy.optimize import minimize_scalar

def objective_call(df, alpha, bid_ask, min_price):
    model_prices =  nassim_price_call(df, alpha, row=bid_ask, min_price = min_price)
    market_prices = df[df[bid_ask] > min_price].sort_values("strike")[bid_ask].to_list()
    return np.sum((np.array(model_prices) - np.array(market_prices))**2)

def objective_puts_raphael(alpha, dataframe, row, min_price):
    _, raphael, _ =  nassim_price_put(dataframe, alpha, row=row, min_price= min_price)
    market_prices = dataframe[dataframe[row] >= min_price].sort_values("strike")[row].to_list()
    return np.sum((np.array(raphael) - np.array(market_prices))**2)

def objective_puts_nassim(alpha, dataframe, row, min_price):
    _, _, nassim =  nassim_price_put(dataframe, alpha, row=row, min_price= min_price)
    market_prices = dataframe[dataframe[row] >= min_price].sort_values("strike")[row].to_list()
    return np.sum((np.array(nassim) - np.array(market_prices))**2)
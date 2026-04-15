import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import warnings

import pricing
import src.dataservices.clean_data as clean_data
import datetime as dt

warnings.filterwarnings("ignore")
matplotlib.use('Agg') 
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 5)

from py_vollib.black_scholes_merton.implied_volatility import implied_volatility
from scipy.optimize import minimize_scalar

"""
Given an data set 

Can you calculate upper and lower bound?
Can you find ATM strike?

Dataset format is as follows:
════════════╤══════════════════════════════════════════════════════════════════════════
Column      │ Description
────────────┼──────────────────────────────────────────────────────────────────────────
Quote_Date  │ Date when the option quote was recorded
close       │ Closing price of the underlying asset
Expire_Date │ Option expiration date
dte         │ Days to expiration
strike      │ Option strike price (used for filtering)
Last        │ Last traded price
Size        │ Trade size
bid         │ Bid price
ask         │ Ask price
right       │ Option type ('put' or 'call')
tau         │ Time to expiration in years
rate        │ Risk-free rate
mid         │ Mid price (average of bid-ask)
IV_ask      │ Implied volatility calculated from ask price
IV_bid      │ Implied volatility calculated from bid price
════════════╧══════════════════════════════════════════════════════════════════════════
"""

def find_spot_price_for_spy(df_puts_filtered):
    spot = float(df_puts_filtered['close'].iloc[0])
    return spot

def find_ATM_strike(df_puts_filtered, spot):
    ATM_strike = pricing.find_ATM_strike(df_puts_filtered, spot)
    return ATM_strike

def calculate_upper_and_lower_bound_of_strike_to_plot(tau, ATM_iv):
    """
    tau means time to expiration
    """
    lower_bound  = spot * np.exp(-3*ATM_iv*np.sqrt(tau))
    higher_bound = spot * np.exp(1*ATM_iv*np.sqrt(tau))
    return lower_bound, higher_bound


df_puts_filtered = pd.read_csv("data/df_puts_2018_filtered.csv")
df_calls_filtered = pd.read_csv("data/df_calls_2018_filtered.csv")
spot = find_spot_price_for_spy(df_puts_filtered)
ATM_strike = find_ATM_strike(df_puts_filtered, spot)

print("spot price is", spot)
print("atm strike price is", ATM_strike)

assert  spot - 1 < ATM_strike < spot + 1, "ATM strike in this region"

ATM_row = df_puts_filtered[df_puts_filtered["strike"] == ATM_strike]
sigma_move = 1
tau  = ATM_row.tau.iloc[0]
ATM_iv = ATM_row["IV_bid"].iloc[0]
lower_bound, higher_bound = calculate_upper_and_lower_bound_of_strike_to_plot(
    tau, ATM_iv
)
print("lower bound atnd upper bound of stikes are {} and {}".format(lower_bound, higher_bound))

filteredPuts = df_puts_filtered[df_puts_filtered.strike <= lower_bound]
filteredCalls = df_calls_filtered[df_calls_filtered.strike >= higher_bound]


min_price = 0.05

result = minimize_scalar(lambda alpha: pricing.objective_call(filteredCalls, alpha, "bid", min_price),
                         bounds=(1, 5), method='bounded')


optimal_call_bid = result.x

result = minimize_scalar(lambda alpha: pricing.objective_call(filteredCalls, alpha, "ask", min_price),
                         bounds=(1, 5), method='bounded')


optimal_call_ask = result.x

optimal_call_ask

pricing.nassim_price_call(filteredCalls, optimal_call_ask, "ask", min_price)

plt.plot(filteredCalls.bid.values, label = "bid")
plt.plot(filteredCalls.ask.values, label = "ask")
plt.plot(pricing.nassim_price_call(filteredCalls, optimal_call_ask, "ask", min_price), label = "nassim ask", color = "black")
plt.savefig("figures/nassim_ask.png")
# plt.plot(pricing.nassim_price_call(filteredCalls, optimal_call_bid, "bid", min_price), label = "bid")
plt.legend()

extrapolate_exp = 0.1
result = minimize_scalar(lambda alpha: pricing.objective_call(filteredCalls, alpha, "ask", extrapolate_exp),
                         bounds=(1, 5), method='bounded')

extrapolate_exp_call_ask = result.x

model_prices = pricing.nassim_price_call(filteredCalls, extrapolate_exp_call_ask, "ask", extrapolate_exp)
strikes      = filteredCalls[filteredCalls["ask"] > extrapolate_exp].sort_values("strike")["strike"].to_list()

def extrapolate_call_prices(df, alpha, min_price, strike_step=5, num_steps=10):
    model_prices = pricing.nassim_price_call(df, alpha, row="ask", min_price=min_price)
    strikes = df[df["ask"] > min_price].sort_values("strike")["strike"].to_list()
    K_anchor = strikes[-1]
    C_anchor = model_prices[-1]

    extrap_strikes = np.arange(K_anchor, K_anchor + strike_step * num_steps, strike_step)
    spot = df["close"].iloc[0]

    extrap_prices = []
    prev_strike = K_anchor
    prev_price = C_anchor

    for K_new in extrap_strikes:
        C_new = ((K_new - spot) / (prev_strike - spot))**(1 - alpha) * prev_price
        extrap_prices.append(C_new)
        prev_strike = K_new
        prev_price = C_new

    return extrap_strikes, extrap_prices

extrapolated = extrapolate_call_prices(filteredCalls, alpha=optimal_call_ask, min_price=extrapolate_exp)

plt.plot(strikes, model_prices, label="Nassim ask (in-sample)", color="red")
plt.plot(extrapolated[0], extrapolated[1], label="Nassim ask (extrapolated)", color="red", linestyle="--")
plt.plot(filteredCalls.strike.values, filteredCalls.bid.values, label = "bid")
plt.plot(filteredCalls.strike.values, filteredCalls.ask.values,label = "ask")
plt.step(filteredCalls.strike.values, filteredCalls.ask.values, where='pre', color="black", label = "ask")
# plt.scatter(filteredCalls.strike.values, filteredCalls.ask.values, color="black")
plt.legend()
plt.show()

"""what part of the distribution to belive?

Tunnel, corrdior, tail
"""

MIN_ = 0.1

result = minimize_scalar(pricing.objective_puts_raphael, bounds=(2, 5),
    method='bounded', args=(df_puts_filtered.copy(), 'ask', MIN_)
)
optimal_alpha_R = result.x

result = minimize_scalar(pricing.objective_puts_nassim, bounds=(2, 5),
    method='bounded', args=(df_puts_filtered.copy(), 'ask', MIN_)
)
optimal_alpha_N = result.x

optimal_alpha_N

strikes = pricing.nassim_price_put(filteredPuts, optimal_alpha_R, row='ask', min_price=MIN_)[0]
raphael = pricing.nassim_price_put(filteredPuts, optimal_alpha_R, row='ask', min_price=MIN_)[1]

strikes_n = pricing.nassim_price_put(filteredPuts, optimal_alpha_N, row='ask', min_price=MIN_)[0]
nassim = pricing.nassim_price_put(filteredPuts, optimal_alpha_N, row='ask', min_price=MIN_)[2]

# alphas = np.linspace(1, 5, 50)
# errors = [objective_puts_raphael(alpha, filteredPuts, 'ask', MIN_) for alpha in alphas]
# plt.plot(alphas, errors, label='Objective Function')
# plt.xlabel('alpha')
# plt.title('Objective Function vs. alpha')

plt.plot(strikes, raphael)
plt.plot(strikes_n, nassim)

plt.plot(filteredPuts.strike.values,
         filteredPuts.ask.values, label = "ask")
plt.plot(filteredPuts.strike.values,
         filteredPuts.bid.values, label = "bid")

plt.legend()

"""- Getting just Nassim ask, because I am not selling anyway
- buying the ask below nassim ask

- 1
"""
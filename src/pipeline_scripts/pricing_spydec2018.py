import pandas as pd
import src.constants as consts
import src.pricingservices.pricing as pricing

def add_interest_rate(df):
    df[consts.INTEREST_RATE] = 0.2
    return df


def subset_columns(df):
    cols = ["Quote_Date", "close", "Expire_Date", "dte", "strike", "Last",
        "Size", "bid", "ask", "right", "tau", "rate", "mid"]
    susbet_df_based_on_columns = df[cols]
    return susbet_df_based_on_columns

def calculate_iv(df):
    df[consts.IV_ASK] = df.apply(pricing.implied_volatilityDF, axis=1, args=('ask',))
    df[consts.IV_BID] = df.apply(pricing.implied_volatilityDF, axis=1, args=('bid',))
    return df

def main():
    df = pd.read_csv("data/spy_eod_201812.csv")
    df = add_interest_rate(df)
    df = subset_columns(df)
    df = calculate_iv(df)
    print(df)

if __name__ == "__main__":
    main()
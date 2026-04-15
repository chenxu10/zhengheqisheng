import pandas as pd 
import datetime as dt

def clean_txt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    header = lines[0].strip().split(",")
    data_lines = [line.strip().split(",") for line in lines[1:]]
    
    df = pd.DataFrame(data_lines, columns=header)
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r'[\[\]]', '', regex=True)
        .str.replace('_', ' ')
        .str.title()
        .str.replace(' ', '_')
    )
    
    common_columns = [
        'Quote_Readtime', 'Quote_Date', 
        'Underlying_Last', 'Expire_Date', 'Dte', 'Strike'
    ]
    
    call_columns = [col for col in df.columns if col.startswith('C_')]
    put_columns = [col for col in df.columns if col.startswith('P_')]
    
    df_calls = df[common_columns + call_columns].copy()
    df_puts = df[common_columns + put_columns].copy()
    df_calls["right"] = "call"
    df_puts["right"] = "put"
    rename_map_calls = {col: col[2:] for col in call_columns}  # Remove "C_"
    rename_map_puts = {col: col[2:] for col in put_columns}    # Remove "P_"
    df_calls.rename(columns=rename_map_calls, inplace=True)
    df_puts.rename(columns=rename_map_puts, inplace=True)

    df_combined = pd.concat([df_calls, df_puts], ignore_index=True)
    df_combined.rename(columns={
        "Underlying_Last": "close",
        "Dte": "dte",
        "Strike": "strike",
        "Bid": "bid",
        "Ask": "ask",
        
    }, inplace=True)
    df_combined["Quote_Readtime"] = pd.to_datetime(df_combined["Quote_Readtime"])
    df_combined["Quote_Date"] = pd.to_datetime(df_combined["Quote_Date"])
    df_combined["Quote_Date"] = df_combined["Quote_Date"].dt.date
    numeric_columns = ["dte", "ask", "bid", "strike", "close"]
    datetime_columns = ["Expire_Date"]
    df_combined[numeric_columns] = df_combined[numeric_columns].apply(pd.to_numeric, errors='coerce')
    df_combined[datetime_columns] = df_combined[datetime_columns].apply(lambda col: pd.to_datetime(col, errors='coerce'))
    df_combined["dte"] = df_combined["dte"].astype(int)
    df_combined["tau"] = df_combined["dte"] / 360
    df_combined["mid"] = 0.5* (df_combined["ask"] + df_combined["bid"])
    return df_combined

def main():
    data = clean_txt("data/spy_eod_201812.txt")
    data.to_csv("data/spy_eod_201812.csv")
    print(data)

if __name__ == "__main__":
    main()

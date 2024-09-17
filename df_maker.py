import pandas as pd
import yfinance as yf
import numpy as np
from datetime import date, datetime

def df_maker(const, coef, start, ticker='BTC-USD'):
    data = yf.Ticker(ticker).history(start=start)
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)  # Reset index to make Date a column
    df['Date'] = df['Date'].dt.date  # Convert Date to date type (removing time)
    df['Date'] = df['Date'].astype(str)
    df = df[['Date', 'Open']]
    # Ensure Date is in datetime format for subtraction
    df['dayth'] = (pd.to_datetime(df['Date']) - pd.to_datetime(date(2010, 7, 19))).dt.days + 561
    df['log2open'] = np.log2(df['Open'])
    df['log2dayth'] = np.log2(df['dayth'])
    df['PredictedLog2Open'] = df['log2dayth']*coef + const
    df['Prediction'] = 2 ** df['PredictedLog2Open']
    return df
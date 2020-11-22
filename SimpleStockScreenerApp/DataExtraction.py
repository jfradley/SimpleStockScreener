import fix_yahoo_finance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
import pandas as pd
import numpy as np

def stock_check(ticker, start, end):
    print(start)
    dfx = pdr.get_data_yahoo(ticker, start, end )
    return dfx


def PriceAnalysis(input_list_df, start, end, ticker_list):
    price_df = pd.DataFrame(columns=['Ticker', 'Last\nprice', 'Pct.\nchange', 'Pct.\nadj.'])

    pct_list = []
    adjusted_pct_list = []

    df_ftse = pdr.get_data_yahoo('^FTSE', start, end)  # FTSE
    inital_ftse = df_ftse['Close'][0]
    print(inital_ftse)
    normalised_ftse = df_ftse['Close'] / inital_ftse
    first_ftse = normalised_ftse[0]
    last_ftse = normalised_ftse[-1]
    pct_ftse = round(((last_ftse - first_ftse) / first_ftse)*100, 3)

    for i, df in enumerate(input_list_df):
        inital = df['Close'][0]
        normalised = df['Close'] / inital
        first = normalised[0]
        last = normalised[-1]
        pct = round(((last - first) / first)*100, 3)
        adjusted_pct = round(pct - pct_ftse, 3)
        pct_list.append(pct)
        adjusted_pct_list.append(adjusted_pct)

    price_df['Ticker'] = ticker_list
    price_df['Pct.\nchange'] = pct_list
    price_df['Pct.\nadj.'] = adjusted_pct_list
    price_df = round(price_df,3)
    return price_df


def VolumeAnalysis(input_list_df, ticker_list):
    volume_df = pd.DataFrame(columns=['Ticker', 'Min.', 'Max.', 'Avg.'])
    volume_list = []
    volume_max_list = []
    volume_min_list = []
    for i, df in enumerate(input_list_df):

        avg = df['Volume'].mean()
        max = df['Volume'].max()
        min = df['Volume'].min()
        volume_list.append(avg)
        volume_max_list.append(max)
        volume_min_list.append(min)
    volume_df['Ticker'] = ticker_list
    volume_df['Avg.'] = volume_list
    volume_df['Max.'] = volume_max_list
    volume_df['Min.'] = volume_min_list
    volume_df = round(volume_df,3)
    return volume_df

def VolatilityAnalysis(input_list_df, ticker_list):

    volatility_df = pd.DataFrame(columns=['Ticker', 'Avg. Pct.', 'Min. Pct.', 'Max. Pct.'])

    average = []
    minimum = []
    maximum = []

    for i, df in enumerate(input_list_df):
        tmp_range = []
        length = len(df)

        high = list(df['High'])
        low = list(df['Low'])
        print(df)
        for i1 in range(0, length):
            print(high[i1])
            tmp_range.append(((high[i1]-low[i1])/((high[i1]+low[i1])/2))*100)

        average.append(np.mean(tmp_range))
        minimum.append(min(tmp_range))
        maximum.append(max(tmp_range))
    volatility_df['Ticker'] = ticker_list
    volatility_df['Avg. Pct.'] = average
    volatility_df['Min. Pct.'] = minimum
    volatility_df['Max. Pct.'] = maximum
    volatility_df = round(volatility_df,3)
    return volatility_df

import fix_yahoo_finance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
import pandas as pd
import numpy as np

def stock_check(ticker, start, end):

    try:
        dfx = pdr.get_data_yahoo(ticker, start, end )
        dfx['Frame'] = 'Pass'
    except:
        data = {'Date': [start], 'Open': [0], 'High':[0], 'Low':[0], 'Close':[0],
                'Adj Close':[0], 'Volume':[0], 'Frame':['Error']}
        dfx = pd.DataFrame(data)
        dfx.set_index('Date', inplace=True)
    print(dfx)
    return dfx


def PriceAnalysis(input_list_df, start, end, ticker_list):

    price_df = pd.DataFrame(columns=['Ticker', 'Last\nprice', 'Pct.\nchange', 'Pct.\nadj.'])

    pct_list = []
    adjusted_pct_list = []
    last_price_list = []

    df_ftse = pdr.get_data_yahoo('^FTSE', start, end)  # FTSE
    inital_ftse = df_ftse['Close'][0]
    normalised_ftse = df_ftse['Close'] / inital_ftse

    first_ftse = normalised_ftse[0]
    last_ftse = normalised_ftse[-1]
    pct_ftse = round(((last_ftse - first_ftse) / first_ftse)*100, 3)

    for i, df in enumerate(input_list_df):
        if df.iloc[0]['Frame'] == 'Pass':

            inital = df['Open'][0]
            normalised = df['Close'] / inital
            first = normalised[0]
            last = normalised[-1]

            try:
                pct = round(((last - first) / first)*100, 3)
            except ZeroDivisionError:
                pct = 0

            adjusted_pct = round(pct - pct_ftse, 3)
            pct_list.append(pct)
            adjusted_pct_list.append(adjusted_pct)
            last_price_list.append(df['Close'][-1])
        else:
            pct_list.append(-100)
            adjusted_pct_list.append(-100)
            last_price_list.append(-100)

    price_df['Ticker'] = ticker_list
    price_df['Last\nprice'] = last_price_list
    price_df['Pct.\nchange'] = pct_list
    price_df['Pct.\nadj.'] = adjusted_pct_list
    price_df = round(price_df, 3)
    return price_df


def VolumeAnalysis(input_list_df, ticker_list):
    volume_df = pd.DataFrame(columns=['Ticker', 'Min.', 'Max.', 'Avg.'])

    volume_list = []
    volume_max_list = []
    volume_min_list = []

    for i, df in enumerate(input_list_df):
        if df.iloc[0]['Frame'] == 'Pass':
            avg = df['Volume'].mean()
            max = df['Volume'].max()
            min = df['Volume'].min()
            volume_list.append(avg/1000)  # change volume unit by a 1000
            volume_max_list.append(max/1000)
            volume_min_list.append(min/1000)
        else:
            volume_list.append(-100)
            volume_max_list.append(-100)
            volume_min_list.append(-100)

    volume_df['Ticker'] = ticker_list
    volume_df['Avg.'] = volume_list
    volume_df['Max.'] = volume_max_list
    volume_df['Min.'] = volume_min_list
    volume_df = round(volume_df, 0)
    return volume_df


def DailyPriceAnalysis(input_list_df, ticker_list):

    volatility_df = pd.DataFrame(columns=['Ticker', 'Avg. Pct.\ndifference',
                                          'Min. Pct.\ndifference',
                                          'Max. Pct.\ndifference'])
    average = []
    minimum = []
    maximum = []

    for i, df in enumerate(input_list_df):
        if df.iloc[0]['Frame'] == 'Pass':
            tmp_range = []
            length = len(df)
            high = list(df['High'])
            low = list(df['Low'])

            for i1 in range(0, length):
                try:
                    pctChange = round((((high[i1]-low[i1])/((high[i1]+low[i1])/2))*100),3)
                    tmp_range.append(pctChange)
                except ZeroDivisionError:
                    pctChange = 0
                    tmp_range.append(pctChange)

            average.append(np.mean(tmp_range))
            minimum.append(min(tmp_range))
            maximum.append(max(tmp_range))

        else:
            average.append(-100)
            minimum.append(-100)
            maximum.append(-100)

    volatility_df['Ticker'] = ticker_list
    volatility_df['Avg. Pct.\ndifference'] = average
    volatility_df['Min. Pct.\ndifference'] = minimum
    volatility_df['Max. Pct.\ndifference'] = maximum

    return volatility_df


def errorRemove(input_list_df,tick_list):
    error_df = pd.DataFrame(columns=['Ticker'])
    error_list = []
    update_list_df = []
    update_tick_list = []
    for i, df in enumerate(input_list_df):
        if df.iloc[0]['Frame'] == 'Error':
            error_list.append(tick_list[i])
        else:

            update_list_df.append(df)
            update_tick_list.append(tick_list[i])

    print(update_list_df)
    error_df['Ticker'] = error_list
    return update_list_df, error_df, update_tick_list


def PriceAnalysis1(input_list_df, ticker_list, area_list):

    price_df = pd.DataFrame(columns=['Ticker', 'Last\nprice', 'Pct.\nchange'])

    pct_list = []
    last_price_list = []
    europe_list = []

    for i, df in enumerate(input_list_df):
        if df.iloc[0]['Frame'] == 'Pass':

            inital = df['Open'][0]
            normalised = df['Close'] / inital
            first = normalised[0]
            last = normalised[-1]

            try:
                pct = round(((last - first) / first)*100, 3)
            except ZeroDivisionError:
                pct = 0

            pct_list.append(pct)
            last_price_list.append(df['Close'][-1])
            print('c')
            if area_list[i] == 'Europe':
                europe_list.append(pct)
        else:
            pct_list.append(-100)
            last_price_list.append(-100)

    europe_ave = np.mean(europe_list)
    ticker_list.append('Europe')
    last_price_list.append(-100)
    pct_list.append(europe_ave)

    price_df['Ticker'] = ticker_list
    price_df['Last\nprice'] = last_price_list
    price_df['Pct.\nchange'] = pct_list
    price_df = round(price_df, 3)
    return price_df
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.pyplot import scatter
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from datetime import timedelta, datetime
import os
import numpy as np

import matplotlib

def avg(a,b,c,d):
    m=(a+b)/2
    n=(c+d)/2
    o=int((m+n)/2)
    return o
def plot_candle_graph():
    N = int(input('input number of days ago: '))
    comp_name = input('Enter the ticker name: ')
    ema1=int(input('enter the short term exponential moving average :'))
    ema2 = int(input('enter the long term exponential moving average :'))

    style.use('ggplot')
    end = dt.datetime.now()
    start = dt.datetime.now() - timedelta(days=N)
    df = web.DataReader(comp_name, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df.to_csv('{}.csv'.format(comp_name))
    # df = df.drop("Symbol", axis=1)

    df = pd.read_csv('{}.csv'.format(comp_name), parse_dates=True, index_col=0)

    # 100 moving average
    df['{}ema'.format(ema1)] = df['Adj Close'].ewm(span=ema1,adjust=False,min_periods=0).mean()
    df['{}ema'.format(ema2)] = df['Adj Close'].ewm(span=ema2, adjust=False,min_periods=0).mean()
    df.dropna(how='any', inplace=True)

    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    buy = []
    buy_date = []
    sell = []
    sell_date = []
    df_sema = df['{}ema'.format(ema1)]
    df_lema = df['{}ema'.format(ema2)]
    for i in range(df['{}ema'.format(ema2)].shape[0]):
        if i == 0:
            if df_sema[i] == 0 and df_lema[i] == 0:
                if df_sema[i + 1] < df_lema[i + 1]:
                    sell.append(df_lema[i])
                    sell_date.append(df.index[i])
                elif df_sema[i + 1] > df_lema[i + 1]:
                    buy.append(df_lema[i])
                    buy_date.append(df.index[i])
        else:
            # short term crocess above long term
            if (df_sema[i - 1] < df_lema[i - 1]) and (df_sema[i] > df_lema[i]):
                o=avg(df_sema[i - 1],df_sema[i],df_lema[i - 1],df_lema[i])
                buy.append(o)
                buy_date.append(df.index[i])
            elif (df_sema[i - 1] > df_lema[i - 1]) and (df_sema[i] < df_lema[i]):
                o=avg(df_sema[i - 1],df_sema[i],df_lema[i - 1],df_lema[i])
                sell.append(o)
                sell_date.append(df.index[i])

    plt.figure(figsize=(20, 10))
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=5, colspan=1, sharex=ax1)  # sharing the x axis of ax1
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    ax1.plot(df.index, df['{}ema'.format(ema1)], color='blue',label='Short term {}EMA'.format(ema1))
    ax1.plot(df.index, df['{}ema'.format(ema2)], color='red',label='Long term {}EMA'.format(ema2))
    ax1.scatter(buy_date,buy,marker=10,color='black',label='BUY')
    ax1.scatter(sell_date, sell, marker=11,color='black',label='SELL')
    ax1.legend()
    # ax1.plot(df.index,df['Adj Close'],color='black')
    os.remove('{}.csv'.format(comp_name))
    plt.show()


plot_candle_graph()

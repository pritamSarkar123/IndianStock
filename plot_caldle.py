import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from datetime import timedelta, datetime
import os


def plot_candle_graph():
    N = int(input('input number of days ago: '))
    comp_name = input('Enter the ticker name: ')
    no_of_mavg = int(input('Number of Moving averages you want to know :'))
    avg = []
    for i in range(no_of_mavg):
        z = int(input('enter the {} th moving average :'.format(i)))
        avg.append(z)

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
    for i in avg:
        df['{}ma'.format(i)] = df['Adj Close'].rolling(window=i, min_periods=0).mean()

    df.dropna(how='any', inplace=True)

    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    plt.figure(figsize=(20, 10))
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=5, colspan=1, sharex=ax1)  # sharing the x axis of ax1
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    for i in avg:
        ax1.plot(df.index, df['{}ma'.format(i)], color='blue')
    # ax1.plot(df.index,df['Adj Close'],color='black')
    os.remove('{}.csv'.format(comp_name))
    plt.show()


plot_candle_graph()

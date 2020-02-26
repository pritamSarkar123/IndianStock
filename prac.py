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
import matplotlib


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
df_sema=df['{}ema'.format(ema1)]
df_lema=df['{}ema'.format(ema2)]
for i in range(df['{}ema'.format(ema2)].shape[0]):
    if i==0:
        if df_sema[i] == 0 and df_lema[i]==0:
            if df_sema[i+1] < df_lema[i+1]:
                sell.append(df_lema[i])
                sell_date.append(df.index[i])
            elif df_sema[i + 1] > df_lema[i + 1]:
                buy.append(df_lema[i])
                buy_date.append(df.index[i])
    else:
        # short term crocess above long term
        if (df_sema[i-1] < df_lema[i-1]) and (df_sema[i] > df_lema[i]):
            buy.append(df_lema[i])
            buy_date.append(df.index[i])
        elif (df_sema[i-1] > df_lema[i-1]) and (df_sema[i] < df_lema[i]):
            sell.append(df_lema[i])
            sell_date.append(df.index[i])

print(buy)
print(buy_date)
print(sell)
print(sell_date)
'''for i in range(df['{}ema'.format(ema2)].shape[0]):
    print(df['{}ema'.format(ema2)][i])'''

'''print(type(df_lema))
print(df_lema.shape)
print(df_lema[0])'''
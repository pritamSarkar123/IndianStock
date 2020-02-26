import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import keras
import matplotlib.pyplot as plt
import os
import datetime as dt
from datetime import date
import pandas_datareader.data as web
from matplotlib import style
import sentiment
from datetime import datetime,timedelta

style.use('ggplot')


def date_prep():
    end=datetime.today()
    start=datetime.today()-timedelta(days=90)
    return start, end


def prepare_csv(comp_name):
    start, end = date_prep()
    try:
        df = web.DataReader(comp_name, 'yahoo', start, end)
        df.to_csv('{}.csv'.format(comp_name), index=False)
    except Exception as e:
        print(e)

def probability_function(predict1, predict2, predict3, predict4, predict5,predict6,predict7):
    p=[]
    c=predict1[0]
    p.append(predict1[1])
    p.append(predict2[1])
    p.append(predict3[1])
    p.append(predict4[1])
    p.append(predict5[1])
    p.append(predict6[1])
    p.append(predict7[1])
    p_p,p_n,p_l=0,0,0
    l=len(p)
    for i in p:
        if i>c:
            p_p=p_p+i
        elif i<c:
            p_l=p_l+i
        else:
            p_n=p_n+i
    p_p=(p_p*100)/(l*c)
    p_l = (p_l * 100) / (l * c)
    p_n = (p_n * 100) / (l * c)

    if p_n == max(p_p,p_l,p_n):
        string="Hold Min Profit"
    elif p_p == max(p_p,p_l,p_n):
        if p_p>=50.00:
            if p_l<=30.00:
                string="Hold For Profit"
            else:
                string="Holding May be Profitable"
        else:
            string = "Holding May be Profitable"
    else:
        if p_l>=50.00:
            if p_p<=30:
                string="Sell Stock"
            else:
                string="You May Hold"
        else :
            string="You May Hold"


    return p_p,p_l,p_n,string
def plot_5_type_pred(predict1, predict2, predict3, predict4, predict5,predict6,predict7, comp_name,profit,loss,nutral,string,posS,negS,nuS):
    plt.figure(figsize=(20, 10))
    plt.plot(predict1, color='red', label='Last Day: {} Next Day: {} by SBIN'.format(predict1[0],predict1[1]))
    plt.plot(predict2, color='blue', label='Last Day: {} Next Day: {} by TCS'.format(predict2[0],predict2[1]))
    plt.plot(predict3, color='yellow', label='Last Day: {} Next Day: {} by WIPRO'.format(predict3[0],predict3[1]))
    plt.plot(predict4, color='pink', label='Last Day: {} Next Day: {} by UNITEDBNK'.format(predict4[0],predict4[1]))
    plt.plot(predict5, color='orange', label='Last Day: {} Next Day: {} by RELIANCE'.format(predict5[0],predict5[1]))
    plt.plot(predict6, color='black',linestyle='-.', label='Last Day: {} Next Day: {} by ^BSESN'.format(predict6[0], predict6[1]))
    plt.plot(predict7, color='black',linestyle='--', label='Last Day: {} Next Day: {} by ^NSEI'.format(predict7[0], predict7[1]))
    plt.title('Next Day Predicted Stock Price of {} probability of profit: {}% loss: {}% nutral: {}% {} moneycontrol pos {} neg {} nut {}'.format(comp_name,profit,loss,nutral,string,posS,negS,nuS))
    plt.xlabel('Time days')
    plt.ylabel('Rupees')
    plt.legend()
    plt.grid(color='black', linestyle='--', linewidth=1)
    #plt.show()
    #path will be changed
    plt.savefig('{}.png'.format(comp_name))

def predict_stock(comp_name):
    #comp_name = input("Enter the company name ")
    comp_name = comp_name.upper()
    prepare_csv(comp_name)
    df = pd.read_csv(comp_name + '.csv')

    value = df.iloc[-60:, ].values
    value_unchanged = df.iloc[-60:, -1].values
    value_last = df.iloc[-1:, -1].values

    sc = MinMaxScaler()
    sc.fit(value)
    value_scaled = sc.fit_transform(value)
    value_scaled = np.array(value_scaled)
    value_scaled = np.reshape(value_scaled, (-1, value_scaled.shape[0], 6))

    sc1 = MinMaxScaler()
    value_unchanged = np.reshape(value_unchanged, (-1, 1))


    sc1.fit(value_unchanged)
    sc1.fit_transform(value_unchanged)

    predict1 = []
    predict1.append(value_last[0])
    for i in range(1,2):
        m = keras.models.load_model('StockPredictorSBIN.NS{}.model'.format(i))
        pred = m.predict(value_scaled)
        pred=sc1.inverse_transform(pred)
        predict1.append(pred[0,0])

    predict2 = []
    predict2.append(value_last[0])
    for i in range(1, 2):
        m = keras.models.load_model('StockPredictorTCS.NS{}.model'.format(i))
        pred = m.predict(value_scaled)
        pred=sc1.inverse_transform(pred)
        predict2.append(pred[0,0])

    predict3 = []
    predict3.append(value_last[0])
    for i in range(1, 2):
        m = keras.models.load_model('StockPredictorWIPRO.NS{}.model'.format(i))
        pred = m.predict(value_scaled)
        pred=sc1.inverse_transform(pred)
        predict3.append(pred[0,0])

    predict4 = []
    predict4.append(value_last[0])
    for i in range(1, 2):
        m = keras.models.load_model('StockPredictorUNITEDBNK.BO{}.model'.format(i))
        pred = m.predict(value_scaled)
        pred=sc1.inverse_transform(pred)
        predict4.append(pred[0,0])

    predict5 = []
    predict5.append(value_last[0])
    for i in range(1, 2):
        m = keras.models.load_model('StockPredictorRELIANCE.NS{}.model'.format(i))
        pred = m.predict(value_scaled)
        pred=sc1.inverse_transform(pred)
        predict5.append(pred[0,0])

    predict6 = []
    predict6.append(value_last[0])
    for i in range(1, 2):
        m = keras.models.load_model('StockPredictor^BSESN{}.model'.format(i))
        pred = m.predict(value_scaled)
        pred = sc1.inverse_transform(pred)
        predict6.append(pred[0, 0])

    predict7 = []
    predict7.append(value_last[0])
    for i in range(1, 2):
        m = keras.models.load_model('StockPredictor^NSEI{}.model'.format(i))
        pred = m.predict(value_scaled)
        pred = sc1.inverse_transform(pred)
        predict7.append(pred[0, 0])

    profit,loss,nutral,string=probability_function(predict1, predict2, predict3, predict4, predict5,predict6,predict7)
    posS,negS,nuS=sentiment.sentiment_analysis("moneycontrol NIFTY",100)
    #posN, negN, nuN = sentiment.sentiment_analysis("NIFTY 50", 100)
    plot_5_type_pred(predict1, predict2, predict3, predict4, predict5,predict6,predict7,comp_name,profit,loss,nutral,string,posS,negS,nuS)
    os.remove(comp_name + '.csv')
    print("completed {}".format(comp_name))


predict_stock('ASHOKLEY.NS')
#predict_stock('ENGINERSIN.NS')
#predict_stock('JINDALSTEL.NS')
#predict_stock('L&TFH.NS')
#predict_stock('PARAGMILK.NS')
#predict_stock('PRAJIND.NS')
#predict_stock('SBIN.NS')
#predict_stock('TATAMOTORS.NS')
#predict_stock('WIPRO.NS')
#predict_stock('ZEEL.NS')
#predict_stock('^NSEI')
'''#predict_stock('AXISBANK.NS')
#predict_stock('ICICIBANK.NS')
#predict_stock('ITC.NS')'''
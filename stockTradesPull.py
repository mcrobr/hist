from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)

tickList = pd.read_csv('sp500.csv', header=None)

for x in list(tickList[1]):
    if x == 'CSCO':
        contract = Stock(x, 'ISLAND', 'USD')
    elif x == 'MSFT':
        contract= Stock(x, 'ISLAND', 'USD')
    else:
        contract = Stock(x, 'SMART', 'USD')
    dt = ''
    barsList = []
    bars = ib.reqHistoricalData(
        contract,
        endDateTime=dt,
        durationStr='2 D',
        barSizeSetting='1 hour',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1)
    barsList.append(bars)
    dt = bars[0].date
    print(x, dt)


    # save to CSV file
    allBars = [b for bars in reversed(barsList) for b in bars]
    df = util.df(allBars)
    df['ticker'] = x
    if os.path.isfile('sp500prices.csv') == True:
        df.to_csv('sp500prices.csv', mode='a', header=False)
    else:
        df.to_csv('sp500prices.csv')

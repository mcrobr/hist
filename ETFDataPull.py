from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)

tickList = pd.read_csv('etf.csv', header=None)

for x in list(tickList[1]):

    contract = Stock(x, 'SMART', 'USD')
    dt = ''
    barsList = []
    bars = ib.reqHistoricalData(
        contract,
        endDateTime=dt,
        durationStr='5 D',
        barSizeSetting='1 day',
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
    if os.path.isfile('etfprices.csv') == True:
        df.to_csv('etfprices.csv', mode='a', header=False)
    else:
        df.to_csv('etfprices.csv')

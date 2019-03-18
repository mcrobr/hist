from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)


tickList = ['TSLA','PLNT','SNBR','DATA','TEAM','CRM','RUN','FIZZ','YETI','AER','FWONK','SPY','EEM']
def getVolume():
    contract = Option('TSLA' , '20190322', 250, 'P', 'SMART')
    hData = ib.reqHistoricalData(contract, '','60 S','1 day','TRADES',True)
    print(hData)

getVolume()






def getOI(tickList):
    for x in tickList:
        contract = Stock(x, 'SMART', 'USD')
        got = ib.reqMktData(contract, "100,101")
        ib.sleep(5)
        print(got)
        print("Ticker:",contract.symbol)
        print("Put Volume:",got.putVolume)
        print("Put OI:",got.putOpenInterest)
        print("Call Volume:",got.callVolume)
        print("Call OI:",got.callOpenInterest)
        print("Req. Time:",got.time)
        oiDF = pd.DataFrame(
            {'ticker': contract.symbol,
             'Put Volume': got.putVolume,
             'Put OI:': got.putOpenInterest,
             'Call Volume:': got.callVolume,
             'Call OI:': got.callOpenInterest,
             'Req. Time:': got.time}, index=[0])
        if os.path.isfile('Open Interest.csv') == True:
            oiDF.to_csv('Open Interest.csv', mode='a', header=False)
        else:
            oiDF.to_csv('Open Interest.csv')
##getOI(tickList)


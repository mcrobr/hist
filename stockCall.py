from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os
####reqMktData is reaching max request type.  Will give dividend info that we can use for the last year but IDK
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)

tickList = pd.read_csv('tickers.csv', header=None)

tL = list(tickList[0])
print(type(tL))
##tickList = ['TSLA','PLNT','SNBR','DATA','TEAM','CRM','RUN','FIZZ','YETI','CVNA','AER','FWONK','SPY','EEM']
def getOI(tL):
    for x in tL:
        contract = Stock(x, 'SMART', 'USD')
        got = ib.reqMktData(contract, "100,456")
        ib.sleep(0.2)
        print(contract.symbol, got.last, got.time, got.dividends)


##        ib.sleep(5)
##        print("Ticker:",contract.symbol)
##        print("Put Volume:",got.putVolume)
##        print("Put OI:",got.putOpenInterest)
##        print("Call Volume:",got.callVolume)
##        print("Call OI:",got.callOpenInterest)
##        print("Req. Time:",got.time)
##        oiDF = pd.DataFrame(
##            {'ticker': contract.symbol,
##             'Put Volume': got.putVolume,
##             'Put OI:': got.putOpenInterest,
##             'Call Volume:': got.callVolume,
##             'Call OI:': got.callOpenInterest,
##             'Req. Time:': got.time}, index=[0])
##        if os.path.isfile('Open Interest.csv') == True:
##            oiDF.to_csv('Open Interest.csv', mode='a', header=False)
##        else:
##            oiDF.to_csv('Open Interest.csv')
getOI(tL)

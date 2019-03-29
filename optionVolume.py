from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)

ticker = 'TSLA'

def getVolume(contract):
    hData = ib.reqHistoricalData(contract, endDateTime='', durationStr='2 D',
        barSizeSetting='30 mins', whatToShow='TRADES', useRTH=True)
    dfExp = pd.DataFrame(columns = ['ticker','expiry','strike','type','bartime','volume','open', 'high','low','close'])
    i = 0
    for x in hData:
        dfExp.loc[i] = [contract.symbol, contract.lastTradeDateOrContractMonth, contract.strike, contract.right, x.date, x.volume, x.open, x.high, x.low, x.close]
        i = i+1
        print(contract.symbol, contract.lastTradeDateOrContractMonth, contract.strike, contract.right, x.date, x.volume, x.open, x.high, x.low, x.close)
    if os.path.isfile('testTicks5.csv') == True:
        dfExp.to_csv('testTicks5.csv', mode='a', header=False)
    else:
        dfExp.to_csv('testTicks5.csv')  

def getStrDate(ticker):
    conId = ib.reqContractDetails(Stock(ticker))[0].contract.conId
    optparams = ib.reqSecDefOptParams(ticker,'','STK', conId)

    global cList
    cList = []
    

    k = 0
    for x in optparams:
        expDates = list(optparams[k].expirations)
        strikes = list(optparams[k].strikes)
        exchange = optparams[k].exchange
        j=0
        while j < len(strikes):
            i=0
            while i < len(expDates):
                cList.append(Option(ticker,expDates[i],strikes[j],'P',exchange))
                i = i+1
            j = j+1
        k = k+1


getStrDate(ticker)
print(len(cList))
##for x in cList:
##    getVolume(x)




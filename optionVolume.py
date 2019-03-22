from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)

ticker = 'PLNT'

def getVolume(contract):
    hData = ib.reqHistoricalData(contract, endDateTime='', durationStr='2 D',
        barSizeSetting='30 mins', whatToShow='TRADES', useRTH=True)
    dfExp = pd.DataFrame(columns = ['ticker','expiry','strike','type','bartime','volume','open', 'high','low','close'])
    i = 0
    for x in hData:
        dfExp.loc[i] = [contract.symbol, contract.lastTradeDateOrContractMonth, contract.strike, contract.right, x.date, x.volume, x.open, x.high, x.low, x.close]
        i = i+1
        print(contract.symbol, contract.lastTradeDateOrContractMonth, contract.strike, contract.right, x.date, x.volume, x.open, x.high, x.low, x.close)
    if os.path.isfile('testTicks.csv') == True:
        dfExp.to_csv('testTicks.csv', mode='a', header=False)
    else:
        dfExp.to_csv('testTicks.csv')  

def getStrDate(ticker):
    conId = ib.reqContractDetails(Stock(ticker))[0].contract.conId
    optparams = ib.reqSecDefOptParams(ticker,'','STK', conId)


    i = 0
    for x in optparams:
        if x.exchange == 'SMART':
            smartCell = i
        else:
            i = i + 1

    expDates = optparams[smartCell].expirations
    strikes = optparams[smartCell].strikes

    returnFun = [expDates, strikes]
    return returnFun

dates = list(getStrDate(ticker)[0])
strikes = list(getStrDate(ticker)[1])
cList = []

j=0
while j < len(strikes):
    i=0
    while i < len(dates):
        cList.append(Option(ticker,dates[i],strikes[j],'P','SMART'))
        i = i+1
    j = j+1
    
for x in cList:
    getVolume(x)




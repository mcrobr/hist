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
    hData = ib.reqHistoricalData(contract, endDateTime='', durationStr='10 D',
        barSizeSetting='30 mins', whatToShow='TRADES', useRTH=True)
    dfExp = pd.DataFrame(columns = ['ticker','expiry','strike','type','bartime','volume','open', 'high','low','close'])
    i = 0
    for x in hData:
        dfExp.loc[i] = [contract.symbol, contract.lastTradeDateOrContractMonth, contract.strike, contract.right, x.date, x.volume, x.open, x.high, x.low, x.close]
        i = i+1
        print(contract.symbol, contract.lastTradeDateOrContractMonth, contract.strike, contract.right, x.date, x.volume, x.open, x.high, x.low, x.close)
    dfExp.to_csv('Ticks.csv')
            
####    print(hData[0].date,hData[1].date,hData[2].date,hData[3].date,hData[4].date,hData[5].date,hData[6].date,hData[7].date,hData[8].date,hData[9].date,hData[10].date,hData[11].date,hData[12].date)
####    print(hData[0].volume,hData[1].volume,hData[2].volume,hData[3].volume,hData[4].volume,hData[5].volume,hData[6].volume,hData[7].volume,hData[8].volume,hData[9].volume,hData[10].volume,hData[11].volume,hData[12].volume)
##getVolume()






def getOI(tickList):
    for x in tickList:
        contract = Stock(x, 'SMART', 'USD')
        got = ib.reqMktData(contract, "100,101")
        ib.sleep(5)
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


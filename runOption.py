from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import optionSpreads

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=3)
##MAC Port 4001



def runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull):
    optionSpreads.getChain(ulType, ulTicker, expDate, expFuture, strikes, timePull)
##    df = pd.read_csv(ulTicker + '_' + expDate + '.csv')  
##    optionSpreads.bearSpreadPuts(df, ulTicker, expFuture, expDate)


ulType = 'Stock'
ulTicker = 'TSLA'
expFuture = '20190315'
expDate = '20190201'
strikes = np.arange(200,405,5)
##timePull = '20190125 20:59:59'
#datetime.datetime.now()
times = ['20190124 20:59:59',
         '20190123 20:59:59',
         '20190122 20:59:59',
         '20190121 20:59:59',
         '20190118 20:59:59',
         '20190117 20:59:59',
         '20190116 20:59:59',
         '20190115 20:59:59',
         '20190114 20:59:59',
         '20190111 20:59:59',
         '20190110 20:59:59',
         '20190109 20:59:59',
         '20190108 20:59:59',
         '20190107 20:59:59']
for x in times:
    runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull = x)

##runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)
##
##ulTicker = 'SPY'
##strikes = np.arange(240,282,2)
##runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)
##
##ulTicker = 'TSLA'
##expDate = '20190208'
##strikes = np.arange(200,405,5)
##runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)
##
##ulTicker = 'SPY'
##strikes = np.arange(240,282,2)
##print(timePull)
##runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)

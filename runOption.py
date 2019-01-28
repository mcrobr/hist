from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import optionSpreads

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=3)
##MAC Port 4001



def runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull):
    
    optionSpreads.getChain(ulType, ulTicker, expDate, expFuture, strikes)

    df = pd.read_csv(ulTicker + '_' + expDate + '_' + timePull + '_ticks.csv')
         
    optionSpreads.bearSpreadPuts(df, ulTicker, expFuture, expDate)


ulType = 'Stock'
ulTicker = 'TSLA'
expFuture = '20190315'
expDate = '20190201'
strikes = np.arange(200,405,5)
timePull = str(datetime.datetime.now())
timePull = timePull[:10]

runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)
ulTicker = 'SPY'
runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)
ulTicker = 'TSLA'
expDate = '20190208'
runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)
ulTicker = 'SPY'
runQuery(ulType, ulTicker, expDate, expFuture, strikes, timePull)

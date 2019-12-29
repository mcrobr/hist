from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os
##NEED TO CORRECT FOR DIVIDENDS - can use historical tick with adjusted price or bring in actuals

df = pd.read_csv('tickerPrices.csv', header=0)
df['date'] = pd.to_datetime(df['date'])
del df['Unnamed: 0']
unique = pd.unique(df['ticker'])
dfRet = pd.DataFrame(index = df['date'])
for i in unique:
    dfx = df['ticker'] == i
    dfy = df[dfx]

    dfy['weekday'] = dfy['date'].dt.weekday
    dfz = dfy[['date','close','ticker']]
    dfz = dfz.set_index('date')
   
    dfz['change'] = dfz['close'].pct_change()


    dfRet[i] = dfz['change']
    
print(dfRet.corr())



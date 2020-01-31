import pandas as pd
import datetime
import numpy as np
import os
from sklearn import svm
##We're taking minute data, and for each minute in each day we're putting in open/high/low/close bar and volume
##Classifying the next close as above or below the current close and running a sklearn classifier on it.
##On two days of SPY data it was 5/10 and guessed 9/10 would be above

df = pd.read_csv('trialMinuteDataMini.csv', index_col = ['date'], parse_dates=['date'],header=0)
df['nextClose'] = np.nan
df['changeClose'] = np.nan
df['ccCategory'] = np.nan
del df['Unnamed: 0']

##Filter down to a day
##For each minute, run a theoretical trade and get the result
##Output timestamp, ticker, day of week, [one, 5, 15, daily] candle [high, low, volume]     date

##Filter down to a day
uniqueDate = list(np.unique(df.index.date))
uniqueTicker = list(df.ticker.unique())


##Cut the dataframe into day slices
dfResults = pd.DataFrame(data = None)
for k in range(len(uniqueTicker)):
    dfOut = pd.DataFrame()
    for i in range(len(uniqueDate)):
        df2 = df[df.index.date == uniqueDate[i]]
        df2 = df2.reset_index()
        df2.nextClose = df2.close.shift(-1)
        df2.changeClose = df2.nextClose / df2.close - 1
        df2.ccCategory = df2.changeClose.map(lambda x: 1 if x < 0 else 0)

        dfOut = dfOut.append(df2)
        dfOut.drop(dfOut.tail(1).index,inplace=True)


dfOut = dfOut.set_index('date')
clf = svm.SVC(gamma=0.001, C=100)
clf.fit(dfOut[['open','high','low','close','volume']][:-10],dfOut.ccCategory[:-10])
print(clf.predict(dfOut[['open','high','low','close','volume']][-10:]))
print(dfOut.tail(10))


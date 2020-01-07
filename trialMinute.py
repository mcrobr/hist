import pandas as pd
import datetime
import numpy as np
import os
##NEED TO CORRECT FOR DIVIDENDS - can use historical tick with adjusted price or bring in actuals

df = pd.read_csv('trialMinuteData.csv', header=0)

df['date'] = pd.to_datetime(df['date'], dayfirst=True)

print(df['date'][0].year)

for i in df.index:
        if df['low'][i] > df['close'][0]*.999 and (df['date'][i].hour < 14 and df['date'][i].minute > 45):
            print("Open")
        elif df['low'][i] > df['close'][0]*.999:
            print("Stopped at ",df['close'][0]*.999," at ",df['date'][i])

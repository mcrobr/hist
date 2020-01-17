import pandas as pd
import datetime
import numpy as np
import os

df = pd.read_csv('trialMinuteData.csv', parse_dates=['date'],header=0)
df['longResult'] = np.nan

##Filter down to a day
##For each minute, run a theoretical trade and get the result
##Output timestamp, ticker, day of week, [one, 5, 15, daily] candle [high, low, volume]     date

##Filter down to a day

uniqueTicker = list(df.ticker.unique())

    ##For each minute, run a theoretical trade and get the result

def longBet(dfIn):
    size = 1
    stopLoss = 1-0.001
    halfSize = 1+0.002
    inPrice = dfIn['close'].iloc[0]
##    dfIn['close'][i+1:end] = closeList
##    dfIn['high'][i+1:end] = highList
##    dfIn['low'][i+1:end] = lowList
##    dfIn['date'][i+1:end] = dateList
    
    ##each time step i want to check for time, stoploss, stopwin
    for x in dfIn.index:

        if size == 0:

            break
        elif dfIn['date'][x] == dfIn['date'].iloc[-1]:

            if size == 1:
                outPrice1 = dfIn['close'][x]
                outPrice2 = dfIn['close'][x]
            elif size == 0.5:
                outPrice2 = dfIn['close'][x]
            break
        elif dfIn['low'][x] <= inPrice * stopLoss:

            if size == 1:
                outPrice1 = inPrice * stopLoss
                outPrice2 = inPrice * stopLoss
                break
            elif size == 0.5:
                outPrice2 = inPrice * stopLoss
                break
        elif size == 1:

            if dfIn['high'][x] >= inPrice * halfSize:

                outPrice1 = inPrice * halfSize
                stopLoss = 1+0.0005
        elif size == 0.5:

            if dfIn['low'][x] >= inPrice * stopLoss:
                outPrice2 = inPrice * stopLoss
                break
    longResult = outPrice1/2 + outPrice2/2 - inPrice
    return longResult


dfResults = pd.DataFrame(data = None)
for k in range(len(uniqueTicker)):
    dfSingleTick = df[df['ticker'] == uniqueTicker[k]]
    
    uniqueDate = list(dfSingleTick.date.dt.date.unique())
    for i in range(len(uniqueDate)):
        df2 = dfSingleTick[dfSingleTick['date'].dt.date == uniqueDate[i]]
        df2 = df2.reset_index()
        
        ##In df2 we need to run longBet and shortBet for each step and record results
        for ind in df2.index:
            ##Make df3 that is a slice of df2 starting at each timestep
            df3 = df2.iloc[ind:-1, :]
            
            df2['longResult'][ind] = longBet(df3)
            
            if ind == df2.index[-2]:
                break
        df2Date = df['date'].dt.date
        dfTicker = df2['ticker'][0]
        dfDate = df2['date'][0].year
        dfDate1 = df2['date'][0].month
        dfDate2 = df2['date'][0].day
        dfResults = dfResults.append(df2, ignore_index=True)
        print(dfTicker, "  ", dfDate,"-",dfDate1,"-",dfDate2)


    
dfResults.to_csv('results.csv')
##dfResults.to_csv('%s_%d%d%d.csv' %(dfTicker, dfDate,dfDate1,dfDate2))


        
            

    
     
##           
####df = df[df['ticker'] == 'SPY']
####df['date'] = pd.to_datetime(df['date'], dayfirst=True)
##def runUD(entryBuffer,slBuffer,halfBuffer):
##    profit = 0
##    uniqueDate = list(df.date.dt.date.unique())
##    for i in range(len(uniqueDate)):
##        df2 = df[df['date'].dt.date == uniqueDate[i]]
##        df2 = df2.reset_index()
##        print(df2.head())
##
##
##        longEntry = df2['close'][0] * (1+entryBuffer)
##        print(longEntry)
##        shortEntry = df2['close'][0] * (1-entryBuffer)
##        print(shortEntry)
##
##        stop = False
##        longed = False
##        shorted = False
##        for x in df2.index:
##            if df2['low'][x] <= shortEntry:
##                print('Short Entered')
##                shorted = True
##                shortTime = df2['date'][x]
##                break
##                
##            elif df2['high'][x] >= longEntry:
##                print('Long Entered at ', longEntry, ' at ', df2['date'][x])
##                longed = True
##                longTime = df2['date'][x]
##                position = 1
##                break
##            
##            else:
##                shorted = False
##                longed = False
##                print('next')
##
##        ##Prices to exit longs and shorts
##        longStopLoss = longEntry * (1-slBuffer)
##        longExitHalf = longEntry * (1+halfBuffer)
##        shortStopLoss = shortEntry * (1+slBuffer)
##        shortExitHalf = shortEntry * (1-halfBuffer)
##
##
##        if longed == True:
##            shares = 1
##            longExitHalfBool = False
##            timesUpBool = False
##            longStopLossBool = False
##            for x in df2[df2['date'] > longTime].index:
##                if (df2['date'][x].hour == 14) and (df2['date'][x].minute > 55):
##                    print("Time's up at ", df2['close'][x], ' at ',df2['date'][x])
##                    timesUpBool = True
##                    priceTimesUp = df2['close'][x]
##                    break
##                elif df2['low'][x] < longStopLoss:
##                    print('Long stopped out at ',longStopLoss, ' at ',df2['date'][x])
##                    longStopLossBool = True
##                    break
##                elif (df2['high'][x] > longExitHalf and longExitHalfBool == False):
##                    print('Half of long exited at ',longExitHalf, ' at ',df2['date'][x])
##                    longExitHalfBool = True
##                    shares = 0.5
##                else:
##                    print('next', df2['date'][x], df2['low'][x+1], df2['date'][x].hour,df2['date'][x].minute )
##            print("Bought 1 at ",longEntry)
##            print("Exited:")
##            if longExitHalfBool == True:
##                print("Half of position at: ", longExitHalf)
##                if timesUpBool == True:
##                    print("Half of position at: ",priceTimesUp)
##                    profit = profit + longExitHalf / 2 + priceTimesUp /2 - longEntry
##                    print('total profit',profit)
##                    print("P&L = :",longExitHalf / 2 + priceTimesUp /2 - longEntry, "(or ",(longExitHalf / 2 + priceTimesUp /2 - longEntry)/longEntry*100,"%)")
##                    
##                elif longStopLossBool == True:
##                    print("Half of position at: ",longStopLoss)
##                    profit = profit + longExitHalf / 2 + longStopLoss /2 - longEntry
##                    print('total profit',profit)
##                    print("P&L = :",longExitHalf / 2 + longStopLoss /2 - longEntry, "(or ",(longExitHalf / 2 + longStopLoss /2 - longEntry)/longEntry*100,"%)")
##            elif longStopLossBool == True:
##                print("Stopped out of full position at: ",longStopLoss)
##                profit = profit + longStopLoss - longEntry
##                print('total profit',profit)
##            elif timesUpBool == True:
##                print("Closed out at the close of day at: ",priceTimesUp)
##                profit = profit + priceTimesUp - longEntry
##                print('total profit',profit)
##                         
##
##    print('total profit',profit)
##    result = [profit, entryBuffer, slBuffer, halfBuffer, uniqueDate, df['ticker'][0]]
##    print(result)
##    resultDF = pd.DataFrame([result], columns=["profit", 'entry buffer','stop loss buffer','half sell buffer','dates','ticker'])
##    if os.path.isfile('dailyResult.csv') == True:
##        resultDF.to_csv('dailyResult.csv', mode='a', header=False)
##    else:
##        resultDF.to_csv('dailyResult.csv')
##
##j = 0
##k = 0
##l = 0
##
##while j < 9:
##    
##    while k < 9:
##        
##        while l < 9:
##            
##            entryBuffer = entryArr[j]
##            slBuffer = slArr[k]
##            halfBuffer = halfArr[l]
##            runUD(entryBuffer,slBuffer,halfBuffer)
##            l = l+1
##        l = 0
##        k = k + 1
##    k = 0
##    j = j+1
##        
##

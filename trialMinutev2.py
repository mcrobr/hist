import pandas as pd
import datetime
import numpy as np
import os

df = pd.read_csv('trialMinuteData.csv', parse_dates=['date'],header=0)

##Filter down to a day
##For each minute, run a theoretical trade and get the result
##Output timestamp, ticker, day of week, [one, 5, 15, daily] candle [high, low, volume]     date

##Filter down to a day
uniqueDate = list(df.date.dt.date.unique())

    ##For each minute, run a theoretical trade and get the result

def longBet(dfIn):
    size = 1
    stopLoss = 1-0.001
    halfSize = 1+0.002
    dfIn['close'][i] = inPrice
    dfIn['close'][i+1:end] = closeList
    dfIn['high'][i+1:end] = highList
    dfIn['low'][i+1:end] = lowList
    dfIn['date'][i+1:end] = dateList
    
    ##each time step i want to check for time, stoploss, stopwin
    for each timestep:
        if size == 0:
            break
        elif last timestep:
            if size == 1:
                outPrice1 = dfIn[x]['close']
                outPrice2 = dfIn[x]['close']
            elif size == 0.5:
                outPrice2 = dfIn[x]['close']
            break
        elif dfIn[x]['low'] <= inPrice * stopLoss:
            if size == 1:
                outPrice1 = inPrice * stopLoss
                outPrice2 = inPrice * stopLoss
            elif size == 0.5:
                outPrice2 = inPrice * stopLoss
        elif size = 1:
            if dfIn[x]['high'] >= inPrice * halfSize:
                outPrice1 = inPrice * halfSize
                stopLoss = 1+0.0005
            else:
        elif size = 0.5:
            if dfIn[x]['low'] >= inPrice * stopLoss:
                outPrice2 = inPrice * stopLoss
                break
            else:
    longResult = outPrice1 + outPrice2 - inPrice
    return longResult


for i in range(len(uniqueDate)):
    df2 = df[df['date'].dt.date == uniqueDate[i]]
    df2 = df2.reset_index()
    df2['longResult'][i] = longBet(df2)
    print(df2['date'][i], df2['longResult'][i])
    df2 = df.iloc[[0, -1]]  ##this makes a new dataframe with the first and last elements
        
            

    
     
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

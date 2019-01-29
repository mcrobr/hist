from ib_insync import *
import pandas as pd
import datetime
import numpy as np
import os

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)
##MAC Port 4001

##ulType = Underlying type of security - uses 'Future' or 'Stock'
ulType = 'Stock'
##ulTicker = Underlying ticker to query
ulTicker = 'TSLA'
##expFuture = Underlying future expiration if applicable
expFuture = '20190315'
##expDate = Expiration date of option
expDate = '20190125'
##strikes = strike prices to query
strikes = np.arange(200,405,5)


print('Option on: ' + ulType)
if ulType == 'Future':
    print('Ticker: ' + expFuture + ' ' + ulTicker)
else:
    print('Ticker: ' + ulTicker)
print('Option Expiry: ' + expDate)
print('Strikes')
print(strikes)





def getChain(ulType, ulTicker, expDate, expFuture, strikes, timePull):
    ##Get ul Contract and Contract ID (ID only needed if we're pulling option chain)
    if ulType == 'Future':
        ulContract = Future(ulTicker, expFuture, 'GLOBEX')
        conId = ib.reqContractDetails(ulContract)[0].contract.conId        
    elif ulType == 'Stock':
        ulContract = Stock(ulTicker, 'SMART', 'USD')
        conId = ib.reqContractDetails(ulContract)[0].contract.conId      
    else:
        print('Underlying type error.  Must be "Future" or "Stock"')

    ##Set up our lists to store the data
    time = []
    pricePutBid = []
    sizePutBid = []
    pricePutAsk = []
    sizePutAsk = []
    priceCallBid = []
    sizeCallBid = []
    priceCallAsk = []
    sizeCallAsk = []
    strikeprice = []

    ##Get the underlying
    ulTick = ib.reqHistoricalTicks(ulContract, '', timePull, 1, 'Bid_Ask',False)
    lastUl = ulTick[-1]
    global time1
    time1 = str(lastUl.time)
    time.append(time1)
    priceCallBid.append(lastUl.priceBid)
    sizeCallBid.append(lastUl.sizeBid)
    priceCallAsk.append(lastUl.priceAsk)
    sizeCallAsk.append(lastUl.sizeAsk)
    pricePutBid.append('NA')
    sizePutBid.append('NA')
    pricePutAsk.append('NA')
    sizePutAsk.append('NA')
    
    strikeprice.append(0)

    if ulType == 'Future':
        for x in strikes:
            try: 
                contract = FuturesOption(ulTicker , expDate, x, 'P', 'GLOBEX')
                tick = ib.reqHistoricalTicks(contract, '', timePull, 1, 'Bid_Ask', False)  
                lastTick = tick[-1]
                time1 = str(lastTick.time)
                time.append(time1)
                pricePutBid.append(lastTick.priceBid)
                sizePutBid.append(lastTick.sizeBid)
                pricePutAsk.append(lastTick.priceAsk)
                sizePutAsk.append(lastTick.sizeAsk)
                strikeprice.append(x)
                contract = FuturesOption(ulTicker , expDate, x, 'C', 'GLOBEX')
                tick = ib.reqHistoricalTicks(contract, '', timePull, 1, 'Bid_Ask', False)  
                lastTick = tick[-1]
                priceCallBid.append(lastTick.priceBid)
                sizeCallBid.append(lastTick.sizeBid)
                priceCallAsk.append(lastTick.priceAsk)
                sizeCallAsk.append(lastTick.sizeAsk)
                print(x)
            except AttributeError:
                print('Strike (or something else) no bueno')
            except IndexError:
                print('IndexError')


    elif ulType == 'Stock':
        for x in strikes:
            try: 
                contract = Option(ulTicker , expDate, x, 'P', 'SMART')
                tick = ib.reqHistoricalTicks(contract, '', timePull, 1, 'Bid_Ask', False)  
                lastTick = tick[-1]
                time1 = str(lastTick.time)
                time.append(time1)
                pricePutBid.append(lastTick.priceBid)
                sizePutBid.append(lastTick.sizeBid)
                pricePutAsk.append(lastTick.priceAsk)
                sizePutAsk.append(lastTick.sizeAsk)
                strikeprice.append(x)
                contract = Option(ulTicker , expDate, x, 'C', 'SMART')
                tick = ib.reqHistoricalTicks(contract, '', timePull, 1, 'Bid_Ask', False)  
                lastTick = tick[-1]
                priceCallBid.append(lastTick.priceBid)
                sizeCallBid.append(lastTick.sizeBid)
                priceCallAsk.append(lastTick.priceAsk)
                sizeCallAsk.append(lastTick.sizeAsk)
                print(x)
            except AttributeError:
                print('Strike (or something else) no bueno')
            except IndexError:
                print('IndexError')

    totalDF = pd.DataFrame(
    {'strike': strikeprice,
     'Call Bid': priceCallBid,
     'Call Ask': priceCallAsk,
     'Call Bid size': sizeCallBid,
     'Call Ask size': sizeCallAsk,
     'Put Bid': pricePutBid,
     'Put Ask': pricePutAsk,
     'Put Bid size': sizePutBid,
     'Put Ask size': sizePutAsk,
     'Time': time})

    if os.path.isfile(ulTicker + '_' + expDate + '.csv') == True:
        totalDF.to_csv(ulTicker + '_' + expDate + '.csv', mode='a', header=False)
    else:
        totalDF.to_csv(ulTicker + '_' + expDate + '.csv')
    global fileName
    fileName = str(ulTicker + '_' + expDate + '.csv')
##Run program


##Do analysis
def bearSpreadPuts(df, ulTicker, expFuture, expDate):

    bspreadBA = []
    sellPutSpreadBA = []
    buyCallSpreadBA = []
    sellCallSpreadBA = []
    s1 = []
    s2 = []
    cdfspread = []
    pdfspread = []
    baCallAvg = (df['Call Ask'] + df['Call Bid']) / 2
    baPutAsk = df['Put Ask']
    baPutBid = df['Put Bid']
    baCallAsk = df['Call Ask']
    baCallBid = df['Call Bid']
    underlyingAvg = str(baCallAvg[0])
    underlyingBid = str(baCallBid[0])
    underlyingAsk = str(baCallAsk[0])

    ##Declare variables for while loop & run while loop to make avg bid ask price
    Strikes = df['strike']
    x = len(Strikes)
    i = 0
    s3 = []
    while i < x-1:
        try:
            s2.append(df['strike'].iloc[i-1])
        except KeyError:
            s2.append(1)
        try:
            s3.append(df['strike'].iloc[i-2])
        except KeyError:
            s3.append(1)
        s1.append(df['strike'].iloc[i])

        i = i+1

    i = 0
    while i < x-1:
        try:
            bspreadBA.append(baPutAsk[i]-baPutBid[i-1])
            sellPutSpreadBA.append(baPutAsk[i-1]-baPutBid[i])
        except KeyError:
            bspreadBA.append(1)
            sellPutSpreadBA.append(1)
        try:
            buyCallSpreadBA.append(baCallAsk[i-1]-baCallBid[i])
            sellCallSpreadBA.append(baCallAsk[i]-baCallBid[i-1])
        except KeyError:
            buyCallSpreadBA.append(1)
            sellCallSpreadBA.append(1)
        i = i+1
               
    avgStrike = (np.array(s1) + np.array(s2))/2
    percBuy = np.divide(bspreadBA,np.subtract(s1, s2))
    percCallBuy = np.divide(buyCallSpreadBA,np.subtract(s1,s2))
    percSell = -np.divide(sellPutSpreadBA,np.subtract(s1, s2))
    percCallSell = -np.divide(sellCallSpreadBA,np.subtract(s1,s2))
    temp = bspreadBA.copy()
    tempCall = buyCallSpreadBA.copy()
    temp.pop(0)
    tempCall.pop(0)
    temp1 = sellPutSpreadBA.copy()
    temp1Call = sellCallSpreadBA.copy()
    temp1.pop()
    temp1Call.pop()
    costCDFBA = np.array(temp) + np.array(temp1)
    costCDFBA = np.insert(costCDFBA,0,"NaN")
    costCallCDFBA = np.array(tempCall) + np.array(temp1Call)
    costCallCDFBA = np.insert(costCallCDFBA,0,"NaN")
    pdfBA = np.divide(np.divide(costCDFBA,np.subtract(s1, s3)),2)
    pdfCallBA = np.divide(np.divide(costCallCDFBA,np.subtract(s1,s3)),2)

    percMid = (percBuy - percSell)/2+percSell
    percCallMid = (percCallBuy - percCallSell)/2+percCallSell
    percBuy = [round(val, 2) for val in percBuy]
    percBuy = ["{0:.0f}%".format(val * 100) for val in percBuy]
    percCallBuy = [round(val, 2) for val in percCallBuy]
    percCallBuy = ["{0:.0f}%".format(val * 100) for val in percCallBuy]
    percSell = [round(val, 2) for val in percSell]
    percSell = ["{0:.0f}%".format(val * 100) for val in percSell]
    percCallSell = [round(val, 2) for val in percCallSell]
    percCallSell = ["{0:.0f}%".format(val * 100) for val in percCallSell]
    percMid = [round(val, 2) for val in percMid]
    percMid = ["{0:.0f}%".format(val * 100) for val in percMid]
    percCallMid = [round(val, 2) for val in percCallMid]
    percCallMid = ["{0:.0f}%".format(val * 100) for val in percCallMid] 
    putSpread = pd.DataFrame(
         {'Strike 1': s2,
         'Strike 2': s1,
         'Bid': percBuy,
         'Ask':percSell,
         'Mid':percMid,
         'Underlying Mid':underlyingAvg}
         )
    callSpread = pd.DataFrame(
        {'Strike 1': s2,
         'Strike 2': s1,
         'Bid': percCallBuy,
         'Ask':percCallSell,
         'Mid':percCallMid,
         'Underlying Mid':underlyingAvg})


    if ulType == 'Future':
        print("Contract: " + ulTicker + " Expiry: " + expFuture)
    else:
        print("Contract: " + ulTicker)

    print("Time:" + df['Time'][0] + "(UTC)")
    print('Underlying Security: ' + ulTicker)
    print('Underlying Midpoint Price: ' + underlyingAvg)

    print("Put Spread")
    print(putSpread[2:].to_string(index=False))
    print("Call Spread")
    print(callSpread[2:].to_string(index=False))
    timePull = str(datetime.datetime.now())
    timePull = timePull[:10]
    if ulType == 'Future':
        putSpread[2:].to_csv(expFuture+ '_' + ulTicker + '_Exp' + expDate + '_Puts_from' + timePull + '.csv')
        callSpread[2:].to_csv(expFuture+ '_' + ulTicker + '_Exp' + expDate + '_Calls_from' + timePull + '.csv')
        
    else:
        putSpread[2:].to_csv(ulTicker + '_Exp' + expDate+'_Puts_from' + timePull +'.csv')
        callSpread[2:].to_csv(ulTicker + '_Exp' + expDate+'_Calls_from' + timePull +'.csv')



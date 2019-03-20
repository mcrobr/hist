from ib_insync import *
import pandas as pd
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)


##Define Inputs - Stock, Date, NEED TO GET CONTRACTID
Ticker = 'VXX'
Expiry = '20190104'
Type = 'P'
startDateTime = '20181218 09:15:00'
endDateTime = ''
numberOfTicks = 1
whatToShow = 'Bid_Ask'
useRth = True

##Go get contract ID, and list of strikes
conId = ib.reqContractDetails(Stock(Ticker))[0].contract.conId
optparams = ib.reqSecDefOptParams(Ticker,'','STK', conId)
print(optparams[7].exchange)
smart = optparams[7]
strikes = []
for x in smart.strikes:
    strikes.append(x)
strikes.sort()
print(strikes)

##Get first contract to set up the dataframe
contract = Option(Ticker, Expiry, strikes[0], Type, 'SMART')
tick = ib.reqHistoricalTicks(contract, startDateTime, endDateTime, numberOfTicks, whatToShow, useRth, ignoreSize=False, miscOptions=None)
df1 = util.df(tick)
try:
    rows = len(df1.index)
    i = 1
    while i < rows:
        df1.drop(df1.index[0], inplace=True)
        i += 1
    df1['Ticker']= Ticker
    df1['Type'] = Type
    df1['Strike'] = strikes[0]
    df1['Expiry'] = Expiry
    print(df1)
except AttributeError:
    print(df1)


##Loop through strike prices
for x in smart.strikes:
    contract = Option(Ticker, Expiry, x, Type, 'SMART')
    print(x)
    tick = ib.reqHistoricalTicks(contract, startDateTime, endDateTime, numberOfTicks, whatToShow, useRth, ignoreSize=False, miscOptions=None)
    df2 = util.df(tick)
    try:
        rows = len(df2.index)
        i = 1
        while i < rows:
            df2.drop(df2.index[0], inplace=True)
            i += 1
        df2['Ticker']= Ticker
        df2['Type'] = Type
        df2['Strike'] = x
        df2['Expiry'] = Expiry
        getit = [df1, df2]
        df1 = pd.concat(getit)
        print(df1)
    except AttributeError:
        print(df1)

##Print to csv
df1.to_csv(Ticker + '_' + Expiry + '_' + Type + '_20181210_ticks.csv')

#from pandas_datareader import data
import pandas as pd
import datetime
import numpy as np
import fix_yahoo_finance as yf
import math

actualToday_=(2019, 5, 13) #YYYY, MM, YY
__today__="2019-05-01" #last month last trading day 
__yearAgo__="2018-06-01" #a year ago as compared to  __today__
__today_daily__ = "2019-06-01"
__yearAgo_daily__ = "2018-05-01"

symbols=["CHD"]
#2. Generate a table of S&P Stocks sorted by 12-month GMS
GMSTable = []

 #calculate for each stock by
for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=None, start=__yearAgo__, end=__today__, interval="1mo", auto_adjust = True, actions=False)
        print(history)

        priceSummary=list(history[history.Close.notnull()]["Close"])
        print(priceSummary)
        #2.1 Get all monthly returns
        returns=[]
        counter=1
        while counter<len(priceSummary)-1:
            returns+=[(priceSummary[counter]-priceSummary[counter-1])/priceSummary[counter-1]]
            counter+=1
        print(returns)
        #2.2 Multiply all monthly returns together and subtract 1
        GMS=1
        for month in returns:
            GMS*=(month+1)
        GMS-=1
        
        GMSTable+=[(symbol,GMS)]
        print(symbol,GMS)
    except:
        print("Ticker:",str(symbol),"raised an error.")

print("GMS by stock calculated. \nCalculating ID for top 50...")

#2.3 Sort by GMS
GMSTable_sorted=sorted(GMSTable, key=lambda x:x[1], reverse=True)

#3. Create a slice with only the top 50
GMS_top50 = GMSTable_sorted[:5]     ##CHANGE THIS

print(GMS_top50)
IDTable=[]
for stock in GMS_top50:
    symbol = stock[0]
   
    ticker = yf.Ticker(symbol)
    history = ticker.history(period=None, start=__yearAgo_daily__, end=__today_daily__, interval="1d", auto_adjust = True, actions=False)
    priceSummary= list(history[history.Close.notnull()]["Close"])
    print(history)
    print(priceSummary)
#calculate ID with ID = sign(Past Return) * [%negative - %positive]
    cNegative, cPositive=0,0
    counter=1
    while counter<len(priceSummary)-1:
            diff=priceSummary[counter]-priceSummary[counter-1]
            if diff>0:
                cPositive+=1
            else:
                cNegative+=1
            counter+=1
    days=len(priceSummary)
    ID = np.sign(stock[1]) * (100*cNegative/days - 100*cPositive/days)
    
    result=stock+(ID,)
    IDTable.append(result)
    print(result)
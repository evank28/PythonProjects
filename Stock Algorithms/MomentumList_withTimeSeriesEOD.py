#from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import quandl
actualToday_=(2019, 5, 13) #YYYY, MM, YY
__today__="2019-04-13" #last month same date
__yearAgo__="2018-04-13" #a year ago as compared to  __today__

##quandl.get_table()


#1. Get a list of S&P stocks
symbols_table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                                header=0)[0]
symbols = list(symbols_table.loc[:, "Symbol"])
#2. Generate a table of S&P Stocks sorted by 12-month GMS
GMSTable = []

 #calculate for each stock by
for ticker in symbols:
    try:
        GMS=1
        dataset="EOD/"+ticker
        #2.1 Get all monthly returns
        historicalReturns = quandl.get(dataset, start_date=__yearAgo__, end_date=__today__, collapse="monthly", transform="rdiff", column_index=11, api_key="dNM8qPBoaYqGgPA-zr-e")# pull the year of data
        
        #2.2 Multiply all monthly returns together and subtract 1
        for month in list(historicalReturns.loc[:,'Adj_Close']):
            GMS*=month
        GMS-=1
        
        GMSTable+=[(ticker,GMS)]
        print(ticker,GMS)
    except:
        print("Ticker: "+ticker+" raised an error.")

   

#2.3 Sort by GMS
GMSTable_sorted=sorted(GMSTable, key=lambda x:x[1])

#3. Create a slice with only the top 50
GMS_top50 = GMSTable_sorted[:50]

print(GMS_top50)
    #calculate ID with ID = sign(Past Return) * [%negative - %positive]

    # sort by ID

#4. Output a slice of the top 25

# from pandas_datareader import data
import os
import numpy as np
import openpyxl
import pandas as pd
import yfinance as yf

actualToday_ = (2019, 5, 13)  # YYYY, MM, YY
__today__ = "2020-01-01"  # last month last trading day
__yearAgo__ = "2019-02-01"  # a year ago as compared to  __today__
__today_daily__ = "2020-01-01"
__yearAgo_daily__ = "2019-02-01"

# 1. Get a list of S&P stocks
print("Downloading Russell 1000 data...")
symbols_table = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index",
                             header=0)[2]
symbols = sorted(list(symbols_table.loc[:, "Ticker"]))  # CHANGE THIS
symbols = [s.replace(".", "-") for s in symbols]

print("Russell 1000 download complete... \nCalculating GMS by stock...")
# 2. Generate a table of S&P Stocks sorted by 12-month GMS
GMSTable = []

# calculate for each stock by
for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=None, start=__yearAgo__, end=__today__,
                                 interval="1mo", auto_adjust=True,
                                 actions=False)

        priceSummary = list(history[history.Close.notnull()]["Close"])
        # 2.1 Get all monthly returns
        returns = []
        counter = 1
        while counter < len(priceSummary) - 1:
            returns += [(priceSummary[counter] - priceSummary[counter - 1]) /
                        priceSummary[counter - 1]]
            counter += 1

        # 2.2 Multiply all monthly returns together and subtract 1
        GMS = 1
        for month in returns:
            GMS *= (month + 1)
        GMS -= 1

        GMSTable += [(symbol, GMS)]
        print(symbol, GMS)
    except:
        print("Ticker:", str(symbol), "raised an error.")

print("GMS by stock calculated. \nCalculating ID for top 50...")

# 2.3 Sort by GMS
GMSTable_sorted = sorted(GMSTable, key=lambda x: x[1], reverse=True)

# 3. Create a slice with only the top 50
GMS_top50 = GMSTable_sorted[:100]  ##CHANGE THIS

print(GMS_top50)
IDTable = []
for stock in GMS_top50:
    symbol = stock[0]
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=None, start=__yearAgo_daily__,
                                 end=__today_daily__, interval="1d",
                                 auto_adjust=False, actions=False)
        priceSummary = list(history[history.Close.notnull()]["Close"].subtract(
            history[history.Open.notnull()]["Open"]))
        # calculate ID with ID = sign(Past Return) * [%negative - %positive]
        cNegative = len([i for i in priceSummary if i < 0])
        cPositive = len([i for i in priceSummary if i > 0])
        """
        cNegative, cPositive = 0,0
        counter=1
        while counter<len(priceSummary)-1:
            diff=priceSummary[counter]-priceSummary[counter-1]
            if diff>0:
                cPositive+=1
            else:
                cNegative+=1
            counter+=1

        """
        days = len(priceSummary)
        ID = np.sign(stock[1]) * (
                100 * cNegative / days - 100 * cPositive / days)

        result = stock + (ID,)
        IDTable.append(result)
        print(result)

    except:
        print("Ticker:", str(symbol), "raised an error.")

# sort by ID
IDTable = sorted(IDTable, key=lambda x: x[2], reverse=False)

# 4. Prepare for instructions output

# open output template
#
#
# template_path = os.getcwd() + "\\StockAlgorithms\\"
# wb = openpyxl.load_workbook(template_path + "instruction_template.xlsx")
# ws = wb.active
#
# # open .csv storing last portfolio
# # TODO: Obtain the last rebalance from a text file
# cur_portfolio_file = file.open(mode='r')
# # Parse to a set
# # TODO: Parsing...
# cur_portfolio = set()

# 5. Output a slice of the top 25
print("\n\nTOP MOMENTUM STOCKS")
i = 0
for i in range(0, 25):  # CHANGE THIS IF MORE THAN 25 STOCKS NEEDED

    print("#" + str(i + 1) + ".", IDTable[i][0],
          "(Details: GMS=" + str(round(IDTable[i][1] * 100, 2)),
          "& ID=" + str(round(IDTable[i][2], 2)) + ")")

# 5. Output a list of buy/sell instructions


# iterate through current 25 and add to an output String for Buy or an Output
# String for Sell or for Keep, respectively
# TODO: Note that this can be done in a single pass as part of step 4


# 6. Save the top 25 list of tickers in a text file for later use
# openpyxl.save("")

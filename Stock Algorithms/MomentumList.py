# from pandas_datareader import data
import os
from operator import itemgetter

import numpy as np
import openpyxl
import pandas as pd
import yfinance as yf

# YYYY, MM, YY
TODAY = "2021-02-01"  # last month last trading day
YEAR_AGO = "2020-03-01"  # a year ago as compared to  TODAY
TODAY_DAILY = "2021-02-01"
YEAR_AGO_DAILY = "2020-03-01"

# 1. Get a list of S&P stocks
print("Downloading Russell 1000 data...")
symbols_table = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index",
                             header=0)[2]
company_pairs = list(zip(list(symbols_table.loc[:, "Ticker"]), list(symbols_table.loc[:, "Company"])))
symbols = sorted(company_pairs, key=itemgetter(0))  # CHANGE THIS
symbols = [(s.replace(".", "-"), company) for s, company in symbols]

print("Russell 1000 download complete... \nCalculating gms by stock...")
# 2. Generate a table of S&P Stocks sorted by 12-month gms
GMS_table = []

# calculate for each stock by
for symbol, company in symbols:
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=None, start=YEAR_AGO, end=TODAY,
                                 interval="1mo", auto_adjust=True,
                                 actions=False)

        price_summary = list(history[history.Close.notnull()]["Close"])
        # 2.1 Get all monthly returns
        returns = []
        counter = 1
        while counter < len(price_summary) - 1:
            returns += [(price_summary[counter] - price_summary[counter - 1]) /
                        price_summary[counter - 1]]
            counter += 1

        # 2.2 Multiply all monthly returns together and subtract 1
        gms = 1
        for month in returns:
            gms *= (month + 1)
        gms -= 1

        GMS_table += [(symbol, company, gms)]
        print(symbol, company, gms)
    except:
        print("Ticker:", str(symbol), "raised an API error.")

print("gms by stock calculated. \nCalculating ID for top 50...")

# 2.3 Sort by gms
GMS_table_sorted = sorted(GMS_table, key=lambda x: x[2], reverse=True)

# 3. Create a slice with only the top 50
GMS_top50 = GMS_table_sorted[:100]  ##CHANGE THIS

print(GMS_top50)
ID_table = []
for stock in GMS_top50:
    symbol = stock[0]
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=None, start=YEAR_AGO_DAILY,
                                 end=TODAY_DAILY, interval="1d",
                                 auto_adjust=False, actions=False)
        price_summary = list(history[history.Close.notnull()]["Close"].subtract(
            history[history.Open.notnull()]["Open"]))
        # calculate ID with ID = sign(Past Return) * [%negative - %positive]
        count_negative = len([i for i in price_summary if i < 0])
        count_positive = len([i for i in price_summary if i > 0])
        """
        count_negative, count_positive = 0,0
        counter=1
        while counter<len(price_summary)-1:
            diff=price_summary[counter]-price_summary[counter-1]
            if diff>0:
                count_positive+=1
            else:
                count_negative+=1
            counter+=1

        """
        days = len(price_summary)
        ID = np.sign(stock[2]) * (
                100 * count_negative / days - 100 * count_positive / days)

        result = stock + (ID,)
        ID_table.append(result)
        print(result)

    except:
        print("Ticker:", str(symbol), "raised an error.")

# sort by ID
ID_table = sorted(ID_table, key=lambda x: x[3], reverse=False)

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

    print("#" + str(i + 1) + ".", ID_table[i][0],
          f"(Details: company={ID_table[i][1]}, gms=" + str(round(ID_table[i][2] * 100, 2)),
          "& ID=" + str(round(ID_table[i][3], 2)) + ")")

# 5. Output a list of buy/sell instructions


# iterate through current 25 and add to an output String for Buy or an Output
# String for Sell or for Keep, respectively
# TODO: Note that this can be done in a single pass as part of step 4


# 6. Save the top 25 list of tickers in a text file for later use
# openpyxl.save("")

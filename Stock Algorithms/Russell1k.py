import pandas as pd

print("Downloading Russell 1000 data...")
symbols_table = pd.read_html("https://en.wikipedia.org/wiki/Russell_1000_Index",
                             header=0)[2]
print(symbols_table)
symbols = sorted(list(symbols_table.loc[:, "Ticker"]))  # CHANGE THIS

print(symbols)

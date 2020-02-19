import pandas as pd 

test = pd.read_html("http://www.cyclingsimulator.com/?page=Riders&pagenumber=1&order=Climbing&sending=desc&nation=Canada&showLowRS=0")

#for i in range(10):

print(test)

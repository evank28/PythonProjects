import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas
import quandl

#plt.figure(figsize=(15,5))

plt.subplot(1,2,1)
plt.plot([1,2,4,5],[1,4,9,16],"go")
plt.plot([1,3],[0,7])
plt.title("My Plot 1")
plt.xlabel("Time (days)")
plt.ylabel("$")

plt.subplot(1,2,2)
plt.plot([5,4,2,1],[1,4,9,16],"go")
plt.plot([3,1],[0,7])
plt.title("My Plot 2")
plt.xlabel("Time (days)")
plt.ylabel("$")

plt.suptitle("The Many Plots")
plt.show()

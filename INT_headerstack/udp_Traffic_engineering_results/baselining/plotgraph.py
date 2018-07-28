from pandas import DataFrame, read_csv

# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number

data = pd.read_csv('INT_udp_flows_results.txt', sep=",", header=None)
data.columns = ["time", "srcip", "dstip", "srcport","dstport","hash","pktlen","swid4","swid3","swid2","swid1","hoplatency4","hoplatency3","hoplatency2","hoplatency1","qdepth4","qdepth3","qdepth2","qdepth1"]
print (data)
print(type(data))
data.plot(x="time",y=["qdepth1"],kind="bar")
plt.show()

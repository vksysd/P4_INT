from pandas import DataFrame, read_csv

# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import numpy as np

df = pd.read_csv('cpu',delim_whitespace=True)
df.columns = ["time","t2","cpu","user","nice","system","iowait","steal","idle"]
x=[]
y=[]
for index,row in df.iterrows():
	#print row["cpu"]
	x.append(index)
	y.append(100-row["idle"])
df1=pd.DataFrame({'time': x,
     'cpu': y,
     })
df1.plot(x='time',y='cpu')
plt.show()

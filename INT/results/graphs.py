import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

x = pd.read_csv('s3_qlength.txt',index_col=None,sep=' ')

print(x.columns)
x.columns = ['Time','Queue Length']
# x.columns = ['Time','Switch Latency']
x.plot(x='Time',y='Queue Length',kind='line')
# x.plot(x='Time',y='Switch Latency',kind='line')
plt.ylabel('Queue Length')
# plt.ylabel('Switch Latency( in microseconds)')
plt.xlabel('Time(in seconds)')
plt.show()
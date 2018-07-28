from pandas import DataFrame, read_csv

# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number

df = pd.read_csv('INT_udp_flows_results.txt', sep=",", header=None)
df.columns = ["time", "srcip", "dstip", "srcport","dstport","hash","pktlen","swid4","swid3","swid2","swid1","hoplatency4","hoplatency3","hoplatency2","hoplatency1","qdepth4","qdepth3","qdepth2","qdepth1"]
time_at_s1 = []
qdepth_at_s1 = []
time_at_s3 = []
qdepth_at_s3 = []
time_at_s4 = []
qdepth_at_s4 = []
time_at_s5 = []
qdepth_at_s5 = []
time_at_s6 = []
qdepth_at_s6 = []
short_flow_pkt_count = 0
long_flow_pkt_count = 0
short_flow_latency_at_s7 = []
long_flow_latency_at_s7 = []
short_flow_latency_at_s3 = []
long_flow_latency_at_s3 = []
short_flow_latency_at_s2 = []
long_flow_latency_at_s2 = []
short_flow_latency_at_s1 = []
long_flow_latency_at_s1 = []
for index,row in df.iterrows():
	if row['swid1'] == 1 :
		qdepth_at_s1.append(row["qdepth1"])
		time_at_s1.append(row["time"])
	if row['swid3'] == 3 :
		qdepth_at_s3.append(row["qdepth3"])
		time_at_s3.append(row["time"])
	if row['swid3'] == 4 :
		qdepth_at_s4.append(row["qdepth3"])
		time_at_s4.append(row["time"])
	if row['swid3'] == 5 :
		qdepth_at_s5.append(row["qdepth3"])
		time_at_s5.append(row["time"])
	if row['swid3'] == 6 :
		qdepth_at_s6.append(row["qdepth3"])
		time_at_s6.append(row["time"])
	if row['srcport'] in range(7000,7060):
		long_flow_pkt_count += 1
		long_flow_latency_at_s7.append(row['hoplatency4'])
		long_flow_latency_at_s3.append(row['hoplatency3'])
		long_flow_latency_at_s2.append(row['hoplatency2'])
		long_flow_latency_at_s1.append(row['hoplatency1'])
	if row['srcport'] in range(50000,50450):
		short_flow_pkt_count += 1
		short_flow_latency_at_s7.append(row['hoplatency4'])
		short_flow_latency_at_s3.append(row['hoplatency3'])
		short_flow_latency_at_s2.append(row['hoplatency2'])
		short_flow_latency_at_s1.append(row['hoplatency1'])
total_short_flow_latency = 0
for i in short_flow_latency_at_s7:
	total_short_flow_latency += i 
for i in short_flow_latency_at_s3:
	total_short_flow_latency += i
for i in short_flow_latency_at_s2:
	total_short_flow_latency += i 
for i in short_flow_latency_at_s1:
	total_short_flow_latency += i  
print("----------- Short flow latency results -------------")
print ("total_short_flow_latency=",total_short_flow_latency)
print("short_flow_pkt_count=",short_flow_pkt_count)
print("avg_short_flow_latency=",total_short_flow_latency/short_flow_pkt_count/1000,"ms")

total_long_flow_latency = 0
for i in long_flow_latency_at_s7:
	total_long_flow_latency += i
for i in long_flow_latency_at_s3:
	total_long_flow_latency += i
for i in long_flow_latency_at_s2:
	total_long_flow_latency += i
for i in long_flow_latency_at_s1:
	total_long_flow_latency += i
print("-----------Long flow latency results -------------")
print ("total_long_flow_latency=",total_long_flow_latency)
print("long_flow_pkt_count=",long_flow_pkt_count)
print("avg_long_flow_latency=",total_long_flow_latency/long_flow_pkt_count/1000,"ms")


	# print (row['time'],row['qdepth3'])
# print(type(data))
# print (qdepth_at_s3)

df1 = pd.DataFrame(
    {'Time in seconds': time_at_s1,
     'Queue depth at S1': qdepth_at_s1,
     })
df1.plot(x='Time in seconds',y='Queue depth at S1')
# df.plot(x="time",y=qdepth_at_s3,kind="bar")
plt.savefig('qdepth_at_s1.png', bbox_inches='tight')

df3 = pd.DataFrame(
    {'Time in seconds': time_at_s3,
     'Queue depth at S3': qdepth_at_s3,
     })
df3.plot(x='Time in seconds',y='Queue depth at S3')
# df.plot(x="time",y=qdepth_at_s3,kind="bar")
plt.savefig('qdepth_at_s3.png', bbox_inches='tight')

# plt.show()
# plt.savefig('qdepth-at_s3.png')

df4 = pd.DataFrame(
    {'Time in seconds': time_at_s4,
     'Queue depth at S4': qdepth_at_s4,
     })
df4.plot(x='Time in seconds',y='Queue depth at S4')
# df.plot(x="time",y=qdepth_at_s3,kind="bar")
plt.savefig('qdepth_at_s4.png', bbox_inches='tight')

df5 = pd.DataFrame(
    {'Time in seconds': time_at_s5,
     'Queue depth at S5': qdepth_at_s5,
     })
df5.plot(x='Time in seconds',y='Queue depth at S5')
# df.plot(x="time",y=qdepth_at_s3,kind="bar")
plt.savefig('qdepth_at_s5.png', bbox_inches='tight')

df6 = pd.DataFrame(
    {'Time in seconds': time_at_s6,
     'Queue depth at S6': qdepth_at_s6,
     })
df6.plot(x='Time in seconds',y='Queue depth at S6')
# df.plot(x="time",y=qdepth_at_s3,kind="bar")
plt.savefig('qdepth_at_s6.png', bbox_inches='tight')

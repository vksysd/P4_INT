import os
import commands
f=open("INT_udp_results.txt","r")
count=3
f1=open("s1.txt","w")
f2=open("s2.txt","w")
f3=open("s3.txt","w")
f4=open("s4.txt","w")
for line in f:
	count=count+1;
	if(count%4==0):
		f4.write(str(line))
	elif(count%4==1):
		f3.write(str(line))
	elif(count%4==2):
		f2.write(str(line))
	else :
		f1.write(str(line))
f.close()
f1.close()
f2.close()
f3.close()
f4.close()
os.system("/home/p4/tutorials/RnD/p4-RnD/distributed/INT_linear_toplogy/INT/results/get_qlength_latency.sh")
os.system("python ./graphs.py")

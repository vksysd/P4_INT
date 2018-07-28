import socket
from datetime import datetime
import os
import sys
import random
from random import choice
import numpy as np
from string import ascii_uppercase
from time import sleep
import random
def randomBytes(n):
    return bytes((''.join(choice(ascii_uppercase) for i in range(n))),'utf-8')
#no_of_bytes_to_send in elephant flows = 1370B
#no_of_bytes_to_send in elephant flows = 10B
#total_exp_time in seconds 
#SOURCE_PORT is the tcp source port of the client
def send_data(total_exp_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER):
	experiment_starts = datetime.now()
	# print("experiment starts at ",experiment_starts)
	# UDP_SERVER = "10.0.8.3"
	# UDP_SERVER = "0.0.0.0"
	if UDP_SERVER == "10.0.8.3" :
		UDP_PORT = 8080
	elif UDP_SERVER == "10.0.8.4" :
		UDP_PORT = 9090
	# UDP_PORT = 8080
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#SOURCE_PORT = 7070
	client.bind(('0.0.0.0', SOURCE_PORT))
	# client.connect((UDP_SERVER, UDP_PORT))
	rand_string = randomBytes(no_of_bytes_to_send)
	# print ("rand_string = ", rand_string)
	#client.sendall(bytes("This is from Client",'UTF-8'))
	total_packets_sent = 0;
	mean = 0.008
	lambd = 1.0/mean
	while (datetime.now() - experiment_starts).total_seconds() < total_exp_time:
		x = client.sendto(rand_string,(UDP_SERVER, UDP_PORT))
		total_packets_sent +=1;
		# print ("client sent ", x ,"bytes")
		#print(".",)
		# in_data =  client.recv(2048)
		# sleep(random.expovariate(lambd))
		delay = 0
		while delay <= 0:
			delay = np.random.normal(mean, 0.1*mean)
			#print("delay = ",delay)
			#lambd = 1.0/mean
			#delay=random.expovariate(lambd)
		sleep(delay)
		# total_packets_sent +=1
		#print("From Server :" ,in_data.decode())
	  	#out_data = input()

	out_data = "bye"
	# print ("sending bye now ", datetime.now())
	# client.sendall(bytes(out_data,'UTF-8'))
	client.sendto(bytes(out_data,'UTF-8'),(UDP_SERVER, UDP_PORT))
	total_packets_sent +=1;
	  #if out_data=='bye':
	  #	break
	client.close()
	# print ("total_packets_sent in this flow = ",total_packets_sent)
	return total_packets_sent



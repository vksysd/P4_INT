import socket
from datetime import datetime
import os
import random
from random import choice
from string import ascii_uppercase
def randomBytes(n):
    return bytes((''.join(choice(ascii_uppercase) for i in range(n))),'utf-8')
#no_of_bytes_to_send in elephant flows = 1370B
#no_of_bytes_to_send in elephant flows = 10B
#total_exp_time in seconds 
#SOURCE_PORT is the tcp source port of the client
def send_data(total_exp_time,no_of_bytes_to_send,SOURCE_PORT):
	experiment_starts = datetime.now()
	print("experiment starts at ",experiment_starts)
	SERVER = "10.0.8.2"
	# SERVER = "0.0.0.0"
	PORT = 8080
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#SOURCE_PORT = 7070
	client.bind(('0.0.0.0', SOURCE_PORT))
	client.connect((SERVER, PORT))
	rand_string = randomBytes(no_of_bytes_to_send)
	print ("rand_string = ", rand_string)
	#client.sendall(bytes("This is from Client",'UTF-8'))
	total_packets_sent = 0;
	while (datetime.now() - experiment_starts).total_seconds() < total_exp_time:
		x = client.send(rand_string)
		#print ("client sent ", x ,"bytes")
		#print(".",)
		in_data =  client.recv(2048)
		total_packets_sent +=1
		#print("From Server :" ,in_data.decode())
	  	#out_data = input()

	out_data = "bye"
	print ("sending bye now ", datetime.now())
	total_packets_sent +=1;
	client.sendall(bytes(out_data,'UTF-8'))
	  #if out_data=='bye':
	  #	break
	client.close()
	print ("total_packets_sent in this flow = ",total_packets_sent)
	return total_packets_sent



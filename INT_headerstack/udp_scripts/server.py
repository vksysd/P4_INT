import socket, threading
import sys
from datetime import datetime
# it gives more throughput as compared to server_multithreaded
if len(sys.argv) < 2:
    print ("./server.py <server_ip>")
    exit(0) 
# UDP_IP = "10.0.8.2"
# UDP_IP = "0.0.0.0"
UDP_IP = str(sys.argv[1])
if UDP_IP == "10.0.8.3" :
    UDP_PORT = 8080
elif UDP_IP == "10.0.8.4" :
    UDP_PORT = 9090
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((UDP_IP, UDP_PORT))
print("Server started on " ,(UDP_IP, UDP_PORT))
print("Waiting for client request..")
total_packets_received = 0;
experiment_start_time = datetime.now()
while True:
    data,address = server.recvfrom(2048)
    # print ("data bytes received =", data)
    msg = data.decode()
    total_packets_received +=1
    if msg=='bye':
        print("last packet from ", address)
        # print( " bye received from client")  
        # break
        #print ("from client", msg)
        if (datetime.now()-experiment_start_time).total_seconds() > 440 :
            print ("total_packets_received till now = ",total_packets_received)

    # y = server.sendto(bytes(msg,'UTF-8'),address)
    # print("y =",y)

    

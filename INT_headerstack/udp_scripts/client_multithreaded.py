import socket
import sys

HOST, PORT = "localhost", 8888
data = " ".join(sys.argv[1:])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(bytes((data + "\n"),'utf-8'), (HOST, PORT))
received = sock.recv(1024)

print("Sent:     {}".format(data))
print("Received: {}".format(received))
#!/usr/bin/env python

import socket

import sys
# TCP_IP = '127.0.0.1'
TCP_IP = socket.gethostbyname(sys.argv[1])
TCP_PORT = 8080
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
SOURCE_PORT = 7070

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', SOURCE_PORT))
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "sent data:", data
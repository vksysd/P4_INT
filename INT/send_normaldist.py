#!/usr/bin/env python3

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import IntField, LongField
from scapy.all import Ether, IP, UDP, TCP

import sys
from random import seed,uniform
import random
import socket
import threading
from time import sleep


from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if len(sys.argv) < 3:
	print("./send.py <client ID> <Experiment Time in seconds>")
	exit(0)

#HOSTNAME = int(sys.argv[1]	)
total_exp_time = int(sys.argv[2])

IFACE = "eth0"
FLOW_THRESHOLD = 50
MIN_SLEEP, MAX_SLEEP = 0.0, 0.3
MIN_PACKET_NUM, MAX_PACKET_NUM = 4, 30
MIN_PACKET_LENGTH, MAX_PACKET_LENGTH = 5,20
CHANGE_FREQUENCY = 5
experiment_starts = datetime.now()
num_threads = 2
np.random.seed(0)

seed(101)
def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

class Flow(threading.Thread):

	def __init__(self, fid):
		threading.Thread.__init__(self)
		self.fid = fid
		self.created_at = datetime.now()
		self.modified_at = datetime.now()

	def run(self):
		fid = self.fid
		subfid = 0
		change_frequency = CHANGE_FREQUENCY
		means = [0.005, 0.05]
		k = 0
		experiment_starts_timestamp = experiment_starts.timestamp()
		addr = socket.gethostbyname(sys.argv[1])
		iface = get_if()
		log = open('timelog/' + str(fid) + '.log', 'w')
		while (datetime.now() - experiment_starts).total_seconds() < total_exp_time:
			subfid += 1
			time_gone = datetime.now() - self.modified_at
			if(time_gone.total_seconds() > total_exp_time/change_frequency):
				self.modified_at = datetime.now()
				k += 1
				#print (time_gone.total_seconds())
				#print ("k = ",k)
				k = k % len(means)
			mean = means[k]
			delay = 0
			while delay <= 0:
				delay = np.random.normal(mean, 0.1*mean)
				#print("delay = ",delay)
				#lambd = 1.0/mean
				#delay=random.expovariate(lambd)
			sleep(delay)
			pkt =  Ether(src=get_if_hwaddr(iface), dst='00:00:00:00:01:01')
			#pkt = pkt /IP(dst=addr) / UDP() / sys.argv[2]
			#pkt = pkt /IP(dst=addr) / TCP(dport=port, sport=random.randint(49152,65535)) / sys.argv[2]
			pkt = pkt /IP(dst=addr) / UDP(dport=1234, sport=random.randint(49152,65535)) / sys.argv[2]
			pkt.show2()
			sendp(pkt, iface=iface, verbose=False)
			log.write(str(datetime.now().timestamp() -
                            experiment_starts_timestamp) + "\n")

		log.close()

def draw_histogram():
	x = []
	for i in range(num_threads):
		#fid = (HOSTNAME * FLOW_THRESHOLD) + i
		with open("timelog/" + str(i) + '.log') as f:
			x += [float(j) for j in f.read().split()]


	x.sort()
	d = pd.DataFrame(x)
	print (d.tail(10))
	#pd.DataFrame(x).
	d.plot(kind='density')
	plt.ylabel('Percentage')
	plt.show()
	print(len(x))

def start_threads():
	# threadLock = threading.Lock()
	threads = []

	for i in range(num_threads):
		try:
			t = Flow(i)
			t.start()
			threads.append(t)
		except:
		   print("Error: unable to start flow")

	for t in threads:
		t.join()

def main():
	start_threads()
	draw_histogram()

if __name__ == '__main__':
	main()

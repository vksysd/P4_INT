import client
import threading
import sys
import time
from datetime import datetime
#elephant flows
total_packets_sent_thread1 = 0
total_packets_sent_thread2 = 0
total_packets_sent_thread3 = 0
total_packets_sent_thread4 = 0

total_exp_time = 450
end_t2 = 0

num_threads = 2;
if len(sys.argv) < 2:
    print ("./server.py <udp_server_ip>")
    exit(0)
class UDPFlow(threading.Thread):
	def __init__(self,threadID):
		threading.Thread.__init__(self)
		self.created_at = datetime.now()
		self.threadID = threadID

	def run(self):
		global total_packets_sent_thread1
		global total_packets_sent_thread2
		global end_t2
		global total_packets_sent_thread3
		global total_packets_sent_thread4

		threadID = self.threadID
		UDP_SERVER = str(sys.argv[1])

		if threadID == 0 :
			# num_elephant_flows = 60
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7000,7000+num_elephant_flows):
				# print ("Sending elephant_flow using Source_port : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread1 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
			print("total_packets_sent_thread1 = ",total_packets_sent_thread1)
			print("total time in thread1 = ",(datetime.now()-time_thread1).total_seconds())
			print ("ending and setting t2")
			end_t2 = 59

			# print ("total_packets_sent_elephant = ",total_packets_sent_elephant)
		# if threadID in range(1,11):
		if threadID == 1:
			time_thread2 = datetime.now()
			num_mouse_flows = 450
			no_of_bytes_to_send = 10
			mouse_flow_time = 0.1
			total_packets_sent_mouse = 0
			upto = 50000+(num_mouse_flows*100)
			for SOURCE_PORT in range(50000,upto):
				if SOURCE_PORT > 50449:
					SOURCE_PORT = 50000+SOURCE_PORT%num_mouse_flows
				# print ("Sending mouse_flow using Source_port : ",SOURCE_PORT)
				# total_packets_sent_mouse += client.send_data(mouse_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread2 += client.send_data(mouse_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread2(short_flows) = ",total_packets_sent_thread2)
			print("total time in thread2 = ",(datetime.now()-time_thread2).total_seconds())

		if threadID == 2 :
			# num_elephant_flows = 60
			time.sleep(5)
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7005,7050):
				print ("Sending elephant_flow using Source_port in thread 3 = : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread3 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread3 = ",total_packets_sent_thread3)
			print("total time in thread3 = ",(datetime.now()-time_thread1).total_seconds())

		if threadID == 3 :
			# num_elephant_flows = 60
			time.sleep(10)
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7000,7045):
				print ("Sending elephant_flow using Source_port in thread 4 = : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread4 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread4 = ",total_packets_sent_thread4)
			print("total time in thread4 = ",(datetime.now()-time_thread1).total_seconds())
		if threadID == 4 :
			# num_elephant_flows = 60
			time.sleep(10)
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7005,7050):
				print ("Sending elephant_flow using Source_port in thread 4 = : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread4 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread5 = ",total_packets_sent_thread4)
			print("total time in thread5 = ",(datetime.now()-time_thread1).total_seconds())
		if threadID == 5 :
			# num_elephant_flows = 60
			time.sleep(20)
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7000,7045):
				print ("Sending elephant_flow using Source_port in thread 4 = : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread4 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread6 = ",total_packets_sent_thread4)
			print("total time in thread6 = ",(datetime.now()-time_thread1).total_seconds())
		if threadID == 6 :
			# num_elephant_flows = 60
			time.sleep(15)
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7005,7045):
				print ("Sending elephant_flow using Source_port in thread 4 = : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread4 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread7 = ",total_packets_sent_thread4)
			print("total time in thread7 = ",(datetime.now()-time_thread1).total_seconds())
		if threadID == 7 :
			# num_elephant_flows = 60
			time.sleep(15)
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7000,7045):
				print ("Sending elephant_flow using Source_port in thread 4 = : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread4 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread8 = ",total_packets_sent_thread4)
			print("total time in thread8 = ",(datetime.now()-time_thread1).total_seconds())
		if threadID == 8 :
			# num_elephant_flows = 60
			time.sleep(15)
			time_thread1 = datetime.now()
			no_of_bytes_to_send = 1370
			elephant_flow_time = 10
			num_elephant_flows = int(total_exp_time/elephant_flow_time)
			total_packets_sent_elephant = 0
			for SOURCE_PORT in range(7000,7045):
				print ("Sending elephant_flow using Source_port in thread 4 = : ",SOURCE_PORT)
				# total_packets_sent_elephant += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
				total_packets_sent_thread4 += client.send_data(elephant_flow_time,no_of_bytes_to_send,SOURCE_PORT,UDP_SERVER)
				if end_t2 == 59:
					break
			print("total_packets_sent_thread9 = ",total_packets_sent_thread4)
			print("total time in thread9 = ",(datetime.now()-time_thread1).total_seconds())

def start_threads():
	threads = []
	for i in range(num_threads):
		try:
			t = UDPFlow(i)
			t.start()
			threads.append(t)
		except:
		   print("Error: unable to start flow")

	for t in threads:
		t.join()
	

def main():

	experiment_start = datetime.now()
	print("experiment starts at ",datetime.now())
	start_threads()
	global total_packets_sent_thread1
	global total_packets_sent_thread2
	print("total_packets_sent_thread1 in main = ",total_packets_sent_thread1)
	print("total_packets_sent_thread2 in main = ",total_packets_sent_thread2)
	print("total_packets_sent_thread3 in main = ",total_packets_sent_thread3)
	print("total_packets_sent_thread4 in main = ",total_packets_sent_thread4)
	total_packets_sent_overall = total_packets_sent_thread1+total_packets_sent_thread2+total_packets_sent_thread3+total_packets_sent_thread4

	print("total packets sent overall = ",total_packets_sent_overall)
	experiment_ends = datetime.now()
	print("total time taken = ", (experiment_ends-experiment_start).total_seconds())
	total_time_taken = (experiment_ends-experiment_start).total_seconds()
	print("avg pkts/sec = ",total_packets_sent_overall/total_time_taken)

if __name__ == '__main__':
	main()

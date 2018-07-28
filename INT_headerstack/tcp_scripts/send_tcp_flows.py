import client

#elephant flows

# num_elephant_flows = 60
num_elephant_flows = 1
# no_of_bytes_to_send = 1370
no_of_bytes_to_send = 10
total_exp_time = 600
total_exp_time = 600
elecphant_flow_time = 1
total_packets_sent = 0
for SOURCE_PORT in range(7011,7011+num_elephant_flows):
	print ("Sending using Source_port : ",SOURCE_PORT)
	total_packets_sent += client.send_data(elecphant_flow_time,no_of_bytes_to_send,SOURCE_PORT)
print ("total_packets_sent = ",total_packets_sent)
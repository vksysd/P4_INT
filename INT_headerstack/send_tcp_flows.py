import client

#elephant flows

num_elephant_flows = 60
no_of_bytes_to_send = 1370
total_exp_time = 600
for SOURCE_PORT in range(7011,7011+num_elephant_flows):
	clinet.send_data(total_exp_time,no_of_bytes_to_send,SOURCE_PORT)
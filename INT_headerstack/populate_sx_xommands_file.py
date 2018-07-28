
# num_elephant_flows = 61
num_elephant_flows = 451
# populate in s1-s6 files the following entries
# table_add ipv4_lpm ipv4_forward 10.0.1.1/32 8080 7070 => 00:00:00:00:01:01 1
# table_add ipv4_lpm ipv4_forward 10.0.8.2/32 7070 8080 => 00:00:00:00:08:02 2
# 7070 is src SOURCE_PORT
# from client perspective 8080 is dst port
# if dst_ip is 10.0.8.3 dst port is 8080
# if dst_ip is 10.0.8.4 dst port is 9090

# SRC_IP = "10.0.1.1"
SRC_IP = "10.0.1.2"

# DST_IP = "10.0.8.3"
# DST_MAC = "00:00:00:00:08:03"
# DST_PORT = 8080

DST_IP = "10.0.8.4"
DST_MAC = "00:00:00:00:08:04"
DST_PORT = 9090

for i in range(1,9):
	file_to_open = "s"+str(i)+"-commands.txt"
	print ("file_to_open = ", file_to_open)
	f1 = open(file_to_open,'a')

	# for SOURCE_PORT in range(7000,7000+num_elephant_flows):
	for SOURCE_PORT in range(50000,50000+num_elephant_flows):

	# for SOURCE_PORT in range(56000):
		print("SOURCE_PORT = ",SOURCE_PORT)
		if i == 7:
			# command_to_write2 = "table_add ipv4_lpm ipv4_forward "+str(DST_IP)+" "+str(SRC_IP)+"/32 "+str(DST_PORT)+" "+str(SOURCE_PORT)+" => 00:00:00:00:01:01 1"
			command_to_write1 = "table_add ipv4_lpm ipv4_forward "+str(SRC_IP)+" "+str(DST_IP)+"/32 "+str(SOURCE_PORT)+" "+str(DST_PORT)+" => "+str(DST_MAC)+" 5"
		elif i == 8 :
			if DST_IP == "10.0.8.3":
				EGRESS_PORT = 1
			elif DST_IP == "10.0.8.4":
				EGRESS_PORT = 2
			# command_to_write2 = "table_add ipv4_lpm ipv4_forward "+str(DST_IP)+" "+str(SRC_IP)+"/32 "+str(DST_PORT)+" "+str(SOURCE_PORT)+" => 00:00:00:00:01:01 3"
			command_to_write1 = "table_add ipv4_lpm ipv4_forward "+str(SRC_IP)+" "+str(DST_IP)+"/32 "+str(SOURCE_PORT)+" "+str(DST_PORT)+" => "+str(DST_MAC)+" "+str(EGRESS_PORT)
		elif i == 1 :
			# command_to_write2 = "table_add ipv4_lpm ipv4_forward "+str(DST_IP)+" "+str(SRC_IP)+"/32 "+str(DST_PORT)+" "+str(SOURCE_PORT)+" => 00:00:00:00:01:01 1"
			command_to_write1 = "table_add ipv4_lpm ipv4_forward "+str(SRC_IP)+" "+str(DST_IP)+"/32 "+str(SOURCE_PORT)+" "+str(DST_PORT)+" => "+str(DST_MAC)+" 3"

		# i= 1 to 6
		else :
			# command_to_write2 = "table_add ipv4_lpm ipv4_forward "+str(DST_IP)+" "+str(SRC_IP)+"/32 "+str(DST_PORT)+" "+str(SOURCE_PORT)+" => 00:00:00:00:01:01 1"
			command_to_write1 = "table_add ipv4_lpm ipv4_forward "+str(SRC_IP)+" "+str(DST_IP)+"/32 "+str(SOURCE_PORT)+" "+str(DST_PORT)+" => "+str(DST_MAC)+" 2"

		#print ("command to write = ", command_to_write1)
		#print ("command to write = ", command_to_write2)
		f1.write(command_to_write1)
		f1.write("\n")
		# f1.write(command_to_write2)
		# f1.write("\n")
	f1.close()

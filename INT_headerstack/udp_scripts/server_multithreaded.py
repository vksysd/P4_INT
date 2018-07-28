import socketserver, threading, time
total_packet_received = 0;
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        global total_packet_received
        total_packet_received+=1;
        #print ("total_packet_received = ",total_packet_received)
        #print("data =",data.decode())
        # print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        if data.decode() == "bye":
            print ("total_packet_received = ",total_packet_received)
        socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == "__main__":
    # HOST, PORT = "0.0.0.0", 8080
    HOST, PORT = "10.0.8.2", 8080

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True: time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
exit()
import socket
from socket import AF_INET, SOCK_DGRAM


client_socket = socket.socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)
server_host = 'localhost'
server_port = 1234
while(True):
       	client_socket.sendto('Message', (server_host, server_port))
  	try:
        	reply, server_address_info = client_socket.recvfrom(1024)
            	print reply
       	except socket.timeout:
		print 'timeouet'

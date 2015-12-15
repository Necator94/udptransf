#serverUDP
import socket  
import sys
import io
import struct
import os


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#host = "10.42.0.15";
host = 'localhost'
port = 5000;
reply = 'foo bar'
 
s.bind((host, port))
i = 0
while(reply) :
        
	d = s.recvfrom(1632)
	reply = d[0]
	addr = d[1]     

	if (reply  == "CLOSE"):
		break

	number = reply[:32] 
	reply = reply[32:]       
	nb = int(number, 2)
	ni = int(bin(i), 2)
	a = []
	k = nb in a	
	
	if (nb == ni) and (k == False) :
		s.sendto('ACK', addr)
		sys.stdout.write(reply)
		a.append(ni)
		
	else :
		s.sendto(str(i), addr)


	i = i + 1
#kek = str(len(reply))
#s.sendto(kek, addr )         

          
s.close()
  

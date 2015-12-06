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

while(reply) :
        
	d = s.recvfrom(1600)
        reply = d[0]
        addr = d[1]     
        
	if (reply  == "CLOSE"):
                break

      	sys.stdout.write(reply)
	


	 # s.sendto(reply, addr )         
         # print reply
          
s.close()
    

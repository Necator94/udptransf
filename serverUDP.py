#serverUDP
import socket  
import sys
import io
import struct
import os


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "10.42.0.15";
port = 5000;
 
s.bind((host, port))



#wr = os.fdopen(sys.stdout.fileno(), 'wb' )

reply = 'foobar'

while(1) :
        d = s.recvfrom(500)
        reply = d[0]
        addr = d[1]     
        if (reply  == "CLOSE"):
                break

      	sys.stdout.write(reply)
	 # s.sendto(reply, addr )         
       # print reply
          
s.close()
    

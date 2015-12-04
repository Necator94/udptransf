#serverUDP
import socket  
import sys
import io
import struct
import os


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "localhost";
port = 5000;
 
s.bind((host, port))



#wr = os.fdopen(sys.stdout.fileno(), 'wb' )



while(1) :
        d = s.recvfrom(500)
        reply = d[0]
        addr = d[1]     
      	sys.stdout.write(reply)
	 # s.sendto(reply, addr )         
       # print reply
          
   
    

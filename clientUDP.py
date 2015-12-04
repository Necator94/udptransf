#clientUDP

import socket  
import sys
import io
import struct
import os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "localhost";
port = 5000;
newin = os.fdopen(sys.stdin.fileno(), 'rb' )
i = 0
while (1):
#	i = i + 1
       # msg = raw_input('Your message: ')       
        kek = newin.read(500)
	s.sendto(kek, (host, port))
       # d = s.recvfrom(1024)
       # reply = d[0]
       # addr = d[1]
         
#        print 'Server reply : ' + reply
     

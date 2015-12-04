#clientUDP

import socket  
import sys
import io
import struct
import os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "10.42.0.15";
port = 5000;
newin = os.fdopen(sys.stdin.fileno(), 'rb' )
kek = "foo bar"
while (kek):
#	i = i + 1
       # msg = raw_input('Your message: ')       
        kek = newin.read(500)
	s.sendto(kek, (host, port))
       # d = s.recvfrom(1024)
       # reply = d[0]
       # addr = d[1]
         
#        print 'Server reply : ' + reply
s.sendto("CLOSE", (host, port))
newin.close()
s.close()

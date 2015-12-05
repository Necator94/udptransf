#clientUDP

import socket  
import sys
import io
import struct
import os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fd = os.fdopen(sys.stdin.fileno(), 'rb' )

host = "10.42.0.15";
port = 5000;
data = "foo bar"

while (data):

        data = fd.read(500)
	s.sendto(data, (host, port))
       # d = s.recvfrom(1024)
       # reply = d[0]
       # addr = d[1]

s.sendto("CLOSE", (host, port))

fd.close()
s.close()

#clientUDP

import socket  
import sys
import io
import struct
import os
import crcmod

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fd = os.fdopen(sys.stdin.fileno(), 'rb' )

#host = "10.42.0.15";
host = 'localhost'
port = 5000;
data = "foo bar"
i = 0 

while (data):
#while (i < 20):
	
	data = fd.read(1600)

	#**************************Packets numeration***************
	bi = bin(i)
	n = bi[2:]
#	print n, ' - number'
	msg = n + data
	lenn = len(n)
#	print (lenn), ' - length of number'
	
	while lenn < 32 :
		msg = '0' + msg
		lenn = lenn + 1
#	print len(msg), ' - length of msg'

	#**********************Buffer creation**********************	
	a = []
	a.append(msg)

	#**********************Sending******************************	
	s.sendto(msg, (host, port))
#	print str(i), ' - number of sended pack'

	#********************Recieving******************************	
	d = s.recvfrom(100)
	reply = d[0] 
	print reply, ' - recieved pack'
	if (reply != 'ACK'):
		
		recvN = int(reply)
		s.sendto(a[recvN], (host, port))
		d = s.recvfrom(100)
		reply = d[0]
		
		if reply != 'ACK2':
			s.sendto(a[recvN], (host, port))
#		else :
#			print 'ACK2'	
			
#	else :
#		print 'ACK'
	i = i + 1


s.sendto("CLOSE", (host, port))

fd.close()
s.close()

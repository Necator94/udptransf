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
indata = "foo bar"

while (indata) :
	
	i = 0 
	a = []					# Buffer creation	
	while (i < 100) :
	
		indata = fd.read(1600)

		#Packets numeration
		bin_i = bin(i)
		cleanNumber = bin_i [2 : ]
		outString = cleanNumber + indata
		lengthOfNumber = len(cleanNumber)

		#Filling free space in the beginning of packet by zeros	
		while lengthOfNumber < 32 :
			outString = '0' + outString
			lengthOfNumber = lengthOfNumber + 1
	
		a.append(outString)			# Adding of new element
		
		s.sendto(outString, (host, port))	# Sendign of outString (packet)
		
		i = i + 1
	
		#********************Recieving******************************	
	recvListOfAcks, addr = s.recvfrom(1632) # Define nessecary size of buffer!!!!!!!!!!!!
		
	ackIdentificator = recvListOfAcks [ : 3] 
	recvListOfAcks = recvListOfAcks [3 : ]
	recvListOfAcks = recvListOfAcks.split()
	if (ackIdentificator == 'ACK') :
		print recvListOfAcks
				


			
#			recvN = int(reply)
		#	s.sendto(a[recvN], (host, port))
	#		d = s.recvfrom(100)
#			reply = d[0]
			
#			if reply != 'ACK2':
#				s.sendto(a[recvN], (host, port))
#			else :
#				print 'ACK2'	
				
#		else :
#			print 'ACK'


s.sendto("CLOSE", (host, port))

fd.close()
s.close()

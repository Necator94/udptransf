#clientUDP

import socket  
import sys
import io
import struct
import os
#import crcmod

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# Socket creation with use of Internet Protocol v4 addresses and datagramms
fd = os.fdopen(sys.stdin.fileno(), 'rb' )			# Open standard input to read binary file

#host = "10.42.0.1";
#host = 'localhost'
host = sys.argv[1]						# Set first argument as a host name
port = int(sys.argv[2])						# Set second argument as a port name
#port = 5000;
indata = "foo bar"						# Set a condition for data transmittion
flag = True

while (indata) :
	
	i = 0 							# Define variable with first meaning
	a = []							# Buffer creation
	while (i < 100) :					# Cycle creation
	
		indata = fd.read(1600)				# Read data with specified buffer size

		#Packets numeration
		bin_i = bin(i)					# Convert from decimal to binary type
		cleanNumber = bin_i [2 : ]			# Get rid of 0x in the beginning of binary
		outString = cleanNumber + indata		# Sum up number of frame with data enclosed
		lengthOfNumber = len(cleanNumber)		# Convert from binary to decimal type

		#Filling free space in the beginning of packet with zeros	
		while lengthOfNumber < 32 :			# Cycle creation
			outString = '0' + outString		# Fulfill with zero till full space of number
			lengthOfNumber = lengthOfNumber + 1	# Move to the next place
	
		a.append(outString)				# Add new element
		
		s.sendto(outString, (host, port))		# Send outString (packet)
		
		i = i + 1					# Move to the next packet
	
		if (flag == True) :
			RTTdata, addr = s.recvfrom(1600)
			s.sendto('triptimedelay',addr)
			flag = False
		#********************Recieving******************************	
	recvListOfAcks, addr = s.recvfrom(1632) 		# Define necessary size of buffer!!!!!!!!!!!!
		
	ackIdentificator = recvListOfAcks [ : 3] 		# Split recvListOfAcks into 2 strings. The first includes ACK
	recvListOfAcks = recvListOfAcks [3 : ]			# The second includes numbers of lost packets
	recvListOfAcks = recvListOfAcks.split()			# Split string by empty spaces
	if (ackIdentificator == 'ACK') :			
		print recvListOfAcks
		if len(recvListOfAcks) == 0 :			# If there are no numbers of lost packets, send ACK RECIEVED
			s.sendto('ACK RECIEVED',addr)
		else :
			for n in recvListOfAcks :		# Otherwise send lost packets back to the server 
				k = int(n)			
				s.sendto(a[k],addr)


		#	recvN = int(reply)
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

#clientUDP

import socket  
import sys
import io
import struct
import os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# Socket creation with the use of Internet Protocol v4 addresses and datagramms
fd = os.fdopen(sys.stdin.fileno(), 'rb' )			# Open standard input to read binary file

#host = "10.42.0.1";
#host = 'localhost'
host = sys.argv[1]						# Set first argument as a host name
port = int(sys.argv[2])						# Set second argument as a port name
#port = 5000;
indata = "foo bar"						# Set a condition for data transmittion
flag = True
sizeOfBlock = 100
while (indata) :
	
	i = 0 							# Define variable with first meaning
	a = []							# Buffer creation
	while (i < sizeOfBlock) :				# Cycle creation
	
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
	
		a.append(outString)				# Add new element to array a[]
		
		s.sendto(outString, (host, port))		# Send outString (packet)
		
		i = i + 1					# Move to the next packet
		
	RTTdata, addr = s.recvfrom(13)				# Recieve packet to determine RTT (it is evaluated by server side) 
	if (RTTdata == 'triptimedelay') :			# If packet contains 'triptimedelay', then send it back
		s.sendto('triptimedelay',addr)
#	print 'triptimedelay'


		#********************Recieving******************************	
	# ADD s.timeout in order to avoid error

	recvListOfAcks, addr = s.recvfrom(1632) 		# Define necessary size of buffer!!!!!!!!!!!! Recieve message with either "ACK" or "ACK + lost packets numbers", store the message in recvListOfAcks
#	print recvListOfAcks		
	ackIdentificator = recvListOfAcks [ : 3] 		# Split recvListOfAcks into 2 strings. The first contains ACK
	recvListOfAcks = recvListOfAcks [3 : ]			# The second contains numbers of lost packets
	recvListOfAcks = recvListOfAcks.split()			# Split string by empty spaces
	if (ackIdentificator == 'ACK') :			
#		print recvListOfAcks
		if len(recvListOfAcks) == 0 :			# If there are no numbers of lost packets, send ACK RECIEVED
			s.sendto('ACK RECIEVED',addr)
#			print 'ack recieved'
		else :
			for n in recvListOfAcks :		# Otherwise send lost packets back to the server 
				k = int(n)			
				s.sendto(a[k],addr)
#				print k, 'index of returned data'


s.sendto("CLOSE", (host, port))					

fd.close()							# Close file descriptor
s.close()							# Close socket

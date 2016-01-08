#clientUDP

import time
t0 = time.time()
import socket  
import sys
import io
import struct
import os


#----------------------------------------Function of packet numeration------------------
def packetNumeration(i, indata):
	outString = bin(i) [2 : ] + indata			# Filling the packet with its number and binary data afterwards
	lengthOfNumber = len(bin(i) [2 : ])			# Packet number assignment
	while lengthOfNumber < 10:				# 'While' loop for fulfilling the rest of packet number space with zeros 
		outString = '0' + outString		
		lengthOfNumber = lengthOfNumber + 1	
	return outString					# Return variable 'outstring' for using in the program


#----------------------------------------The main body of program------------------

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# Socket creation with the use of Internet Protocol v4 addresses and datagramms
fd = os.fdopen(sys.stdin.fileno(), 'rb' )			# Open standard input to read binary file

if len(sys.argv) != 3:						# Error handling of wrong arguments assignment
	print 'Error! Need to pass ip-adress and port number as arguments'
	sys.exit(1)
else:
	host = sys.argv[1]					# Set first argument as a host name
	port = int(sys.argv[2])					# Set second argument as a port name
indata = "foo bar"						# First setting of a condition for data transmittion
sizeOfBlock = 1000						# Number of packets sent to server at once. Chosen in experiments	
dataCounter = 0							# Setting of variable for futher counting of all data sent


while (indata) :
	i = 0 							# Define variable for counting up to 400 
	a = []							# Buffer creation
	while i < sizeOfBlock:					# Cycle for sending block of packets (400)
		indata = fd.read(1422)				# Read data with specified buffer size
		dataCounter += len(indata)			# Counting all coming out data
		dataString = packetNumeration(i, indata)	# Call a function to assign number of packet and add binary data in packet
		a.append(dataString)				# Add new element to array a[]. Used for futher resending of lost packets
		s.sendto(dataString, (host, port))		# Send packet to server
		i += 1						# Move to the next packet
	while True:						# Cycle for recieving and sending acknoledgement, packet for RTT determination
		ackList, addr = s.recvfrom(1432)		# Recieving data and wrinting it in 'ackList' variable from 'addr' IP-address
		if ackList == 'triptimedelay':			# If packet contains 'triptimedelay', then send it back
			s.sendto('triptimedelay',addr)
	
		if ackList[:4] == 'SACK':			# If packet contains 'SACK', send ACK RECIEVED
			s.sendto('ACK RECIEVED',addr)
			break

		if ackList[:3] == 'ACK' :			# Otherwise, sending lost packets back to the server 
			for n in ackList[3:].split():					
				s.sendto(a[int(n)], addr)

k = 0
while k < 5 :
	s.sendto('CLOSE', (host, port))
	k += 1

fd.close()							# Close file descriptor
s.close()							# Close socket
print '------------------------------------------------'	
print '|  Bytes transfered: ', dataCounter			# Show size of data sent to server
t = round(time.time() - t0, 2)
print '|  Execution time:   ', t,'s' 				# Calculate and show execution time
avgSpeed = round(dataCounter/t / 1024 / 1024,2)
if avgSpeed < 1 :
	avgSpeed = round(dataCounter/t / 1024,2)		# Calculate and show data rate
	print '|  Average speed:    ', avgSpeed, 'Kb/s'		# in kbps
else :
	print '|  Average speed:    ', avgSpeed, 'Mb/s'		# in Mbps
print '------------------------------------------------'

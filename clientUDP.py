#clientUDP
import time
t0 = time.time()
import socket  
import sys
import io
import struct
import os
#----------------------------------------------------------
def packetNumeration(i, indata):
	#Packets numeration
	outString = bin(i) [2 : ] + indata		# Sum up number of frame with data enclosed
	lengthOfNumber = len(bin(i) [2 : ])		# Convert from binary to decimal type
	#Filling free space in the beginning of packet with zeros	
	while lengthOfNumber < 32:			# Cycle creation
		outString = '0' + outString		# Fulfill with zero till full space of number
		lengthOfNumber = lengthOfNumber + 1	# Move to the next place
	return outString
#----------------------------------------------------------

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# Socket creation with the use of Internet Protocol v4 addresses and datagramms
fd = os.fdopen(sys.stdin.fileno(), 'rb' )			# Open standard input to read binary file
logs = open('logs.txt', 'w')

if len(sys.argv) < 3:
	print 'Error! Need to pass ip-adress and port number as arguments'
	sys.exit(1)
else:
	host = sys.argv[1]						# Set first argument as a host name
	port = int(sys.argv[2])						# Set second argument as a port name
indata = "foo bar"						# Set a condition for a data transmittion
sizeOfBlock = 400
dataCounter = 0
t = 1.5
while (indata) :
	i = 0 							# Define variable with first meaning
	a = []							# Buffer creation
	logs.write('BEGIN of main While'+'\n')
	while i < sizeOfBlock:				# Cycle creation
		indata = fd.read(1400)				# Read data with specified buffer size
		dataCounter += len(indata)
		dataString = packetNumeration(i, indata)
		a.append(dataString)				# Add new element to array a[]
		s.sendto(dataString, (host, port))		# Send outString (packet)
		logs.write(str(i)+'\n')
		i += 1						# Move to the next packet
	logs.write('END of main while'+'\n')	
	while True:
		ackList, addr = s.recvfrom(1432)
		logs.write(ackList + '....recieved string'+'\n')
		if ackList == 'triptimedelay':			# If packet contains 'triptimedelay', then send it back
			s.sendto('triptimedelay',addr)
			logs.write(str(ackList) + '....triptimedelay'+'\n')
	
		if ackList[:4] == 'SACK':		# If there are no numbers of lost packets, send ACK RECIEVED
			t = int(int(ackList [4:32], 2)) / 1000000.0
			#if t < 0.02:
			#	t *= 10
		#	t *= 10 
			s.sendto('ACK RECIEVED',addr)
			logs.write('ACK RECIEVED was sent to server'+'\n')
			break

		if ackList[:3] == 'ACK' and len(ackList[32:]) != 0:
			for n in ackList.split()[32:]:		# Otherwise send lost packets back to the server 			
				s.sendto(a[int(n)], addr)
 				logs.write(str(n) + '....index of returned data'+'\n')
	logs.write('end of wile true'+'\n')
	if t < 0.02:
		s.settimeout(t)
		try:
			ackList, addr = s.recvfrom(1432)
			if ackList[:4] == 'SACK':
				s.sendto('ACK RECIEVED',addr)
		except socket.timeout:
			foo = 'bar'
	s.settimeout(None)
s.sendto("CLOSE", (host, port))					
logs.write('CLOSE sent'+'\n')
logs.close()
fd.close()							# Close file descriptor
s.close()
print '------------------------------------------------'							# Close socket
print '|  Bytes transfered: ', dataCounter
t = round(time.time() - t0, 2)
print '|  Execution time:   ', t,'s' 
avgSpeed = round(dataCounter/t / 1024 / 1024,2)
if avgSpeed < 1 :
	avgSpeed = round(dataCounter/t / 1024,2)
	print '|  Average speed:    ', avgSpeed, 'Kb/s'
else :
	print '|  Average speed:    ', avgSpeed, 'Mb/s'
print '------------------------------------------------'

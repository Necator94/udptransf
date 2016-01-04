#serverUDP
import socket  
import sys
import io
import struct
import os
import time
#------------------------------------------------------------------------
def defTripTime(addr, t):
	s.settimeout(t)
	t0 = time.time()
	s.sendto('triptimedelay', addr)
	while True:
		try :
			indata, addr = s.recvfrom(13)
       			if (indata == 'triptimedelay') :
            			t = (time.time() - t0)
				if t < 0.02:
					t *= 100 
				return t
				break
		except socket.timeout:
			t0 = time.time()
	         	s.sendto('triptimedelay', addr)
#------------------------------------------------------------------------
# Search of empty spaces (not recieved packets) in data array, creation of a string with lost packets for sending and lost packets amount calculation   
def lookForNone(dataArray) :						# Have dataArray - recieved strings as input argument
	lostPackets = 'ACK'						# Identifying word in the begining of the string 
	n_cycles = 0							# Initialization of variable with amount of lost packets
	for index, element in enumerate(dataArray) :			# index - array element index, element - array string content
     		if element == None:					# Check on 'None' existing in string of array (None means packet lost) 
			lostPackets = lostPackets + str(index) + ' '	# Formation of the string for sending to client
			n_cycles += 1					# Append another '1' (another packet lost)
	return lostPackets, n_cycles					# Retun of the strings to main programm
#------------------------------------------------------------------------
# Positive acknowlage creation for the client (timeout information included)
def ackToClient(t):							# Have t - timeout as input argument of function
	outStr = bin(int(round(t * 1000000))) [2 : ]                	# Creation of a string with current value of timeout in binary string format
   	lenNumber = len(bin(int(round((t * 1000000)))) [2 : ])        	# Timeout value length definition in bytes
#Filling free space in the middle of packet with zeros       
        while lenNumber < 28 :                    			# Cycle creation
		outStr = '0' + outStr          				# Fulfill with zero till full space of number
        	lenNumber += 1		    				# Move to the next place
	outStr = 'SACK' + outStr 					# Finall string formation for sending
	return outStr							# Return of the string to main program
#------------------------------------------------------------------------

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logs = open('logs.txt', 'w')

host = '0.0.0.0'
port = 5000;
indata = 'foo bar'
t = 2.2 
sizeOfBlock = 400

s.bind((host, port))
logs.write('START OF PROGRAMM'+ '\n') 
while indata:
	n_cycles = 0
	i = 0
	dataArray = [None] * sizeOfBlock
	numbersArray = []
	logs.write('BEGIN of main while'+'\n')
        while i < sizeOfBlock:
		try :
			indata, addr = s.recvfrom(1432)
			if indata == "CLOSE":
				logs.write('CLOSE recieved'+'\n'+'exit(0)'+'\n')
				exit(0)
		
			dataArray[int(int(indata[:32], 2))] = indata[32:]
			logs.write(str(i)+'   - number of iteration|    '+ (str(int(int(indata[:32], 2))))+'   - index of recieved packet'+'\n')
			i += 1	
		except socket.timeout :
			logs.write(str(i)+'....amount of recieved packets, timeout reached')
			break		
	logs.write('END of main while'+'\n')
	t = defTripTime(addr, t)
	logs.write(str(t)+'....triptime'+ '\n')
	lostPackets, n_cycles = lookForNone(dataArray)
	logs.write('lookForNone|   '+str(lostPackets)+'  - lostPackets|    '+ str(n_cycles)+'   - n_cycles'+'\n')
	s.settimeout(t)
	if n_cycles > 0:
		s.sendto(lostPackets, addr)
		logs.write(str(lostPackets)+'....lost packets sent to client after cycle 1'+'\n')

		while n_cycles > 0:

			logs.write('begin of ebota'+ '\n')
			try :
				indata, addr = s.recvfrom(1432)
				if indata != 'ACK RECIEVED':
					logs.write(str(int(int(indata[:32], 2))) + '.....index of recieved lost packet 1 attempt'+ '\n')
					dataArray[int(int(indata[:32], 2))] = indata[32:]
			except socket.timeout:
				s.sendto(lostPackets, addr)
				logs.write(str(lostPackets)+'.....first timeout in ebota, packet list sent again 2'+ '\n')

			lostPackets, n_cycles = lookForNone(dataArray)
			logs.write('lookForNone|   '+str(lostPackets)+'  - lostPackets|    '+ str(n_cycles)+'   - n_cycles'+'\n')
	if n_cycles == 0:
		s.sendto(ackToClient(t), addr)
		logs.write(str(ackToClient(t))+'....ack + timeout'+'\n')
 		logs.write('if '+str(n_cycles)+' == 0'+ '\n') 
		while True:
			try:
				indata, addr = s.recvfrom(1432)
				logs.write(str(indata)+'.....positive ACK from client1 '+ '\n')
				if indata == 'ACK RECIEVED' or len(indata[32:]) != 0:
					break	
			except socket.timeout:
				s.sendto(ackToClient(t), addr)
				logs.write(str(lostPackets)+'.....timeout in hueta, packet list sent again'+ '\n')
	logs.write('WRITING to file'+ '\n')
	k = 0
	while k < sizeOfBlock:
		if dataArray[k] == None:
			logs.write(str(k)+'   - index of None packet' + '\n'+ 'exit(0)')	
			exit(0)
		
		sys.stdout.write(dataArray[k])
		k += 1
        logs.write('END of writing to file'+ '\n') 
logs.write('END OF PROGRAMM'+ '\n')	
s.close()
  

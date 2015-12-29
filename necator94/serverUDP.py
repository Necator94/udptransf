#serverUDP
import socket  
import sys
import io
import struct
import os
import time
#------------------------------------------------------------------------
def splitting(indata):
	innumber = indata [ : 32] 
	indata = indata [32 : ]       
	binNumber = int(innumber, 2)
	packetIndex = int(binNumber) 
	return packetIndex,indata
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
					t *= 1.5 
				return t
				break
		except socket.timeout:
			t0 = time.time()
	         	s.sendto('triptimedelay', addr)
#------------------------------------------------------------------------
def lookForNone(dataArray) :
	lostPackets = 'ACK'
	n_cycles = 0	
	for index, element in enumerate(dataArray) :
     		if element == None:
			lostPackets = lostPackets + str(index) + ' '
			n_cycles = n_cycles + 1
	return lostPackets, n_cycles
#------------------------------------------------------------------------
def ackToClient(t):	
	outString = bin(int(round(t * 1000000))) [2 : ]                 # Sum up number of frame with data enclosed
   	lengthOfNumber = len(bin(int(round((t * 1000000)))) [2 : ])               # Convert from binary to decimal type
        #Filling free space in the beginning of packet with zeros       
        while lengthOfNumber < 28 :                     # Cycle creation
		outString = '0' + outString             # Fulfill with zero till full space of number
        	lengthOfNumber = lengthOfNumber + 1     # Move to the next place
	outString = 'SACK' + outString 
	return outString

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logs = open('logs.txt', 'w')

host = '0.0.0.0'
port = 5000;
indata = 'foo bar'
t = 2 
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
		
			packetIndex, indata = splitting(indata)
			dataArray[packetIndex] = indata
			logs.write(str(i)+'   - number of iteration|    '+ str(packetIndex)+'   - index of recieved packet'+'\n')
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
					packetIndex, indata = splitting(indata)
					logs.write(str(packetIndex)+'.....index of recieved lost packet 1 attempt'+ '\n')
					dataArray[packetIndex] = indata
			except socket.timeout:
				s.sendto(lostPackets, addr)
				logs.write(str(lostPackets)+'.....first timeout in ebota, packet list sent again 2'+ '\n')

			lostPackets, n_cycles = lookForNone(dataArray)
			logs.write('lookForNone|   '+str(lostPackets)+'  - lostPackets|    '+ str(n_cycles)+'   - n_cycles'+'\n')

	
	if n_cycles == 0:
		ack = ackToClient(t)
		s.sendto(ack, addr)
		logs.write(str(ack)+'....ack + timeout'+'\n')
 		logs.write('if '+str(n_cycles)+' == 0'+ '\n') 
		while True:
			try:
				indata, addr = s.recvfrom(1432)
				logs.write(str(indata)+'.....positive ACK from client1 '+ '\n')
				if indata == 'ACK RECIEVED':
					break	
			except socket.timeout:
				s.sendto(ack, addr)
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
  

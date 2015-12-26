#serverUDP
import socket  
import sys
import io
import struct
import os
import time

def splitting(indata):
	innumber = indata [ : 32] 
	indata = indata [32 : ]       
	binNumber = int(innumber, 2)
	packetIndex = int(binNumber) 
	return packetIndex,indata

def defTripTime(addr, t) :
	s.settimeout(t)
	t0 = time.time()
	
	s.sendto('triptimedelay', addr)
	try :
		indata, addr = s.recvfrom(13)
        	if (indata == 'triptimedelay') :
            		t = (time.time() - t0) * 4 
			return t
	except socket.timeout:
         	s.sendto('triptimedelay', addr)
		try :
			indata, addr = s.recvfrom(13)
               		if (indata == 'triptimedelay') :
	                	t = (time.time() - t0) * 4 
				return t
		except socket.timeout:
			s.sendto('triptimedelay', addr)

def lookForNone(dataArray) :
	lostPackets = 'ACK'
	n_cycles = 0	
	for index, element in enumerate(dataArray) :
     		if element == None:
			lostPackets = lostPackets + str(index) + ' '
			n_cycles = n_cycles + 1
	return lostPackets, n_cycles

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = '0.0.0.0'
port = 5000;
indata = 'foo bar'
t = 0.02 
sizeOfBlock = 100

s.bind((host, port))

while(indata) :
	Ncycles = 0
	i = 0
	dataArray = [None] * sizeOfBlock
	numbersArray = []
        while (i < sizeOfBlock) :
		try :
			indata, addr = s.recvfrom(1632)
			if (indata == "CLOSE"):
				exit(0)
		
			s.settimeout(t)
			packetIndex, indata = splitting(indata)
			dataArray[packetIndex] = indata
#			print packetIndex, ' index of recieved packet'
			i = i + 1	
		except socket.timeout :
#			print i, ' excepted index'
			zz = 0	
	t = defTripTime(addr, t)
	lostPackets, n_cycles = lookForNone(dataArray)
	
	s.sendto(lostPackets, addr)
#	print lostPackets, '   list of lost'
	s.settimeout(t)
	l = 0
#	print n_cycles, 'Ncycles'
	if (n_cycles > 0): 		
		while (l < n_cycles) :
#			print n_cycles, '    - in while  - n_cycles'
#			print l , '         - in while - l'
			try :
				indata, addr = s.recvfrom(1632)
				if (indata != 'ACK RECIEVED') :
					packetIndex, indata = splitting(indata)
#					print packetIndex, ' - try 1'
					dataArray[packetIndex] = indata
			except socket.timeout:
				lostPackets, n_cycles = lookForNone(dataArray)
				l = -1
				s.sendto(lostPackets, addr)
#				print 'ahtung1'
				try : 
					indata, addr = s.recvfrom(1632)
               				if (indata != 'ACK RECIEVED') :
						packetIndex, indata = splitting(indata)
 #                    				print packetIndex, ' - try 2'
						dataArray[packetIndex] = indata
					
				except socket.timeout:
			        	lostPackets, n_cycles = lookForNone(dataArray)
                                	l = -1	
					s.sendto(lostPackets, addr)
#					print 'ahtung2'
			l = l + 1
	else:
		indata, addr = s.recvfrom(1632)
#		print indata , ' -  kek'
	k = 0
	while (k < sizeOfBlock) :
		if (dataArray[k] == None) :
			exit(0)
		
		sys.stdout.write(str(dataArray[k]))
		k = k + 1
          
s.close()
  

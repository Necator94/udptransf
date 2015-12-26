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
            		t = (time.time() - t0) * 2 
			return t
	except socket.timeout:
         	s.sendto('triptimedelay', addr)
		try :
			indata, addr = s.recvfrom(13)
               		if (indata == 'triptimedelay') :
	                	t = (time.time() - t0) * 2
				return t
		except socket.timeout:
			s.sendto('triptimedelay', addr)
#	except socket.timeout:
#                s.sendto('triptimedelay', addr)
#                indata, addr = s.recvfrom(13)
#                if (indata == 'triptimedelay') :
#                        t = (time.clock() - t0) * 5000
#                        return t

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#host = "10.42.0.15";
host = '0.0.0.0'
port = 5000;
indata = 'foo bar'
lostPackets = 'ACK'
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
			packetIndex, indata = splitting(indata)
			dataArray[packetIndex] = indata
			if (indata == "CLOSE"):
				exit(0)
		
		except socket.timeout :
			lostPackets = lostPackets + str(i) + ' '
			Ncycles = Ncycles + 1
		i = i + 1
#	t = defTripTime(addr, t)

	s.sendto(lostPackets, addr)
	print lostPackets, '   list of lost'
	s.settimeout(t)
	l = 0
	print Ncycles, 'Ncycles'
	if (Ncycles == 0):
		try :
			indata, addr = s.recvfrom(1632)
                        if (indata != 'ACK RECIEVED') :
 	                	packetIndex, indata = splitting(indata)
                        	print packetIndex
                               	dataArray[packetIndex] = indata
               	except socket.timeout:
                        s.sendto(lostPackets, addr)
                       	try :
                        	indata, addr = s.recvfrom(1632)
                        	if (indata != 'ACK RECIEVED') :
               		         	packetIndex, indata = splitting(indata)
                                	print packetIndex
                                	dataArray[packetIndex] = indata
 
                    	except socket.timeout:
                       		s.sendto(lostPackets, addr)
 		
	else:
		while (l < Ncycles) :
		
			try :
				indata, addr = s.recvfrom(1632)
				if (indata != 'ACK RECIEVED') :
			
					packetIndex, indata = splitting(indata)
					print packetIndex, ' - try 1'
					dataArray[packetIndex] = indata
			except socket.timeout:
				s.sendto(lostPackets, addr)
				try : 
					indata, addr = s.recvfrom(1632)
               				if (indata != 'ACK RECIEVED') :
						packetIndex, indata = splitting(indata)
                     				print packetIndex, ' - try 2'
						dataArray[packetIndex] = indata
					
				except socket.timeout:
			        	s.sendto(lostPackets, addr)
		l = l + 1
#	print l, ' - l'

	k = 0
#	while (k < sizeOfBlock) :
#		if (dataArray[k] == None) :
#			exit(0)
		
#		sys.stdout.write(str(dataArray[k]))
#		k = k + 1
          
s.close()
  

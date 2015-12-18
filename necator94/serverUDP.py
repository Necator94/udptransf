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

def lookForNone(dataArray):
	lostPackets = 'ACK '
	for k in range(len(dataArray)):
		if dataArray[k] == None:  lostPackets = lostPackets + str(k) + ' '
	return lostPackets


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#host = "10.42.0.15";
host = '10.42.0.1'
port = 5000;
indata = 'foo bar'
lostPackets = 'ACK'
flag = True
s.bind((host, port))
while(indata) :
	i = 0
	dataArray = [None] * 100
	numbersArray = []
        while (i < 100) :
		indata, addr = s.recvfrom(1632)

		if (indata == "CLOSE"):
			break

		packetIndex, indata = splitting(indata)
		dataArray[packetIndex] = indata
		print '43'
		if (packetIndex != i) :
			lostPackets = lostPackets + str(i) + ' '
			print '46'
		if (flag == True) :
			print '48'
			s.settimeout(2.2)
			t0 = time.clock()
			s.sendto('triptimedelay', addr)
			print '51'		
			try :
              			print '54'
				indata, addr = s.recvfrom(1632)
               			if (indata == 'triptimedelay') :
                      			t = time.clock() - t0
					flag = False
       					print '59'
			except socket.timeout:
               			s.sendto('triptimedelay', addr)
				indata, addr = s.recvfrom(1632)
                                if (indata == 'triptimedelay') :
                                        t = time.clock() - t0
					flag = False
	print '66'
	i = i + 1
	s.sendto(lostPackets, addr)
	s.settimeout(t + 0.2)
	try :
		indata, addr = s.recvfrom(1632)
		if (indata != 'ACK RECIEVED') :
			packetIndex, indata = splitting(indata)
			dataArray[packetIndex] = indata
	except socket.timeout:
		s.sendto(lostPackets, addr)
		indata, addr = s.recvfrom(1632)
                if (indata != 'ACK RECIEVED') :
                        packetIndex, indata = splitting(indata)
                        dataArray[packetIndex] = indata
	
#	k = 0
#	while (k < 100) :
#		if (dataArray[k] == None) :
#			exit(0)
		
#		sys.stdout.write(dataArray[k])
#		k = k + 1
          
s.close()
  

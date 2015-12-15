#serverUDP
import socket  
import sys
import io
import struct
import os


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#host = "10.42.0.15";
host = 'localhost'
port = 5000;
indata = 'foo bar'
 
s.bind((host, port))
while(indata) :
	i = 0
	lossPackets = 'ACK '
	numbersArray = []
	dataArray = []
        while (i < 100) :
		indata, addr = s.recvfrom(1632)

		if (indata == "CLOSE"):
			break

		innumber = indata [ : 32] 
		indata = indata [32 : ]       
	
		binNumber = int(innumber, 2)
		bini = int(bin(i), 2)
	

		k = binNumber in numbersArray	
	
		if (binNumber == bini) and (k == False) :
		#	s.sendto('ACK', addr)		# dont foget to remove
			numbersArray.append(bini)
			dataArray.append(indata)
		else :
			lossPackets = lossPackets + str(i) + ' '
	

		i = i + 1


	s.sendto(lossPackets, addr)

	k = 0
	while (k < 100) :
		sys.stdout.write(dataArray[k])
		k = k + 1
#kek = str(len(reply))
#s.sendto(kek, addr )         

          
s.close()
  

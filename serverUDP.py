#serverUDP
import socket  
import sys
import io
import struct
import os
import time
#------------------------------------------------------------------------
# Defenition of trip time delay for timeout setting 
def defTripTime(addr, t):						# addr - ip adress that uses for sending, t - uses for setting of timeout
	defTripTime.func_code = (lambda addr, t:t).func_code		# This string allows to call function only once
	s.settimeout(t)							# Set t as timeout
	t0 = time.time()						# Time measuring of process begining
	s.sendto('triptimedelay', addr)					# Sending message, for trip time delay checking  
	while True:
		try :			
			indata, addr = s.recvfrom(13)			# Trying of recieving specific message
       			if (indata == 'triptimedelay') :
            			t = (time.time() - t0)			# Calculation of trip time delay
				if t < 0.02:				# Check on minimal time which provides effective work
					t *= 10				# If triptime too small, coefficient 10 will be used
				else:
					t *= 1.2			
				return t
				break
		except socket.timeout:					# If message is not recieved message sends again
			t0 = time.time()				# Resetting time of process begining
	         	s.sendto('triptimedelay', addr)			# Send message again
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
while True:
	closekek = True							# Flag which uses for closing of main cycle
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# Opening of UDP socket
	logs = open('logs.txt', 'w')					
	host = '0.0.0.0'						# Acception of connections from any adresses
	port = 5000;							# Number of port which will be used
	indata = 'foo bar'						# Assigning of 'empty' string (uses for cycle condition)
	t = 1.5 							# Starting timeout (uses before trip time delay definition)
	sizeOfBlock = 400						# Amount of packets which will be process during one cycle
	s.bind((host, port))						
	logs.write('START OF PROGRAMM'+ '\n') 
	while indata:							# Start of main cycle
		n_cycles = 0						# Initialization of nessesative variables
		i = 0
		dataArray = [None] * sizeOfBlock			# Initialization of empty "None" array with certain size
		logs.write('BEGIN of main while'+'\n')
        	while i < sizeOfBlock:					# Execute cycle untill 400 packets will be recieved
			try :
				indata, addr = s.recvfrom(1432)		# Recieving of data string from client
				s.settimeout(t)				# Setting of timeout
				if indata == "CLOSE":			# Check on last message from client
					logs.write('CLOSE recieved'+'\n'+'exit(0)'+'\n')
					closekek = False		# Changing of flag status
					break				# Cycle interraption
		
				dataArray[int(int(indata[:10], 2))] = indata[10:]	# Write "clean" data with recieved index to array 
				logs.write(str(i)+'   - number of iteration|    '+ (str(int(int(indata[:10], 2))))+'   - index of recieved packet'+'\n')
				i += 1					# Counter of recieved packets
			except socket.timeout :				# In case of timeout break the cycle
				logs.write(str(i)+'....amount of recieved packets, timeout reached')
				break	
		if closekek == False:					# Check flag on last recived message
			s.close()
			break						# Breaking of cycle
		logs.write('END of main while'+'\n')
		t = defTripTime(addr, t)				# Calling the function for trip time delay definition
		logs.write(str(t)+'....triptime'+ '\n')
		lostPackets, n_cycles = lookForNone(dataArray)		# Check array on empty strings
		logs.write('lookForNone|   '+str(lostPackets)+'  - lostPackets|    '+ str(n_cycles)+'   - n_cycles'+'\n')
		s.settimeout(t)						# Setting of timeout
		if n_cycles > 0:					# If data array is not full 
			s.sendto(lostPackets, addr)			# Sending of string with lost packeges
			logs.write(str(lostPackets)+'....lost packets sent to client after cycle 1'+'\n')

			while n_cycles > 0:				# Untill the data array will be full
				logs.write('begin of ebota'+ '\n')
				try :
					indata, addr = s.recvfrom(1432)	# Reciving of lost packet
					if indata == "CLOSE":		# Checking on last message from client
						logs.write('CLOSE recieved'+'\n'+'break in n_cycles > 0'+'\n')
						break
					if indata != 'ACK RECIEVED':	# If revieved message is not positive ack 
						logs.write(str(int(int(indata[:10], 2))) + '.....index of recieved lost packet 1 attempt'+ '\n')
						dataArray[int(int(indata[:10], 2))] = indata[10:] # Write lost packet to array
				except socket.timeout:			# If data is not recieved
					s.sendto(lostPackets, addr)	# Sending of list with lost packets again
					logs.write(str(lostPackets)+'.....first timeout in ebota, packet list sent again 2'+ '\n')

				lostPackets, n_cycles = lookForNone(dataArray) # Check on empty strings in array
				logs.write('lookForNone|   '+str(lostPackets)+'  - lostPackets|    '+ str(n_cycles)+'   - n_cycles'+'\n')
		if n_cycles == 0:					# If all all packets resieved and array is full
 			logs.write('if '+str(n_cycles)+' == 0'+ '\n') 
			s.sendto('SACK', addr)				# Sending of positive ack to client
			logs.write('SACK'+'....ack to client'+'\n')
			while True:					# Untill the positive ack will be recieved 
				try:
					indata, addr = s.recvfrom(1432)	
					if indata == "CLOSE":		# Check on last message from client
						logs.write('CLOSE recieved'+'\n'+'break in n_cycles == 0'+'\n')
						break
					logs.write(str(indata)+'.....positive ACK from client1 '+ '\n')
					if indata == 'ACK RECIEVED' or len(indata[10:]) !=0 : # If positive ack or packet with data was recieved
						break	
				except socket.timeout:
					s.sendto('SACK', addr)		# Sending of positive ack to client again
					logs.write('SACK'+'.....timeout in hueta, packet list sent again'+ '\n')
	
		logs.write('WRITING to file'+ '\n')
		k = 0
		while k < sizeOfBlock:					# Cycle for passing of data array to output stream 
			if dataArray[k] == None:			# If data array is not full, emergency exit from program
				logs.write(str(k)+'   - index of None packet' + '\n'+ 'exit(0)')	
				exit(1)		
			sys.stdout.write(dataArray[k])			# Writing of element with k index to std output stream
			k += 1						# Counter of strings
    		logs.write('END of writing to file'+ '\n') 
	logs.write('END OF PROGRAMM'+ '\n')	
	s.close()							# Close socket
  

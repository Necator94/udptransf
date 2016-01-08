
#clientTCP
import socket        
            
host = 'localhost' 
port = 5000                
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while(1):

	msg = raw_input('Your message:  ')
	s.send(msg)
	reply= s.recv(1024)
	print 'Server answer: ' + reply

s.close()

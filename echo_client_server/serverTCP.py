#serverTCP

import socket               
 
host="localhost"
port = 5000  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
             
s.bind((host, port))        
s.listen(5)

(c, (ip, Port)) = s.accept()
                
while(1):
     
	data=c.recv(1024)
	print 'Client message: ' + data  
	c.send(data)

c.close()
s.close()





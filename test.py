import sys
import io
import struct
import os


newin = os.fdopen(sys.stdin.fileno(), 'rb' )
f = open('myfile.jpg','wb')

i = 0
#while i < 1000: 
	
kek = newin.read()
f.write(kek)
#i = i + 1

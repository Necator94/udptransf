import sys
import io
import struct
import os

#sys.stdin = open(sys.stdin.fileno(), 'r', <new settings>)
#data = open(sys.stdin.read())
#data = sys.stdin.read(16)
#f = sys.stdin.read()
#keke = f.read

#reader = io.open(sys.stdin.fileno())
#reader = io.open(sys.stdin.read())

#file = open(sys.stdin.read, 'r')
#bytes  = file.read( )

#buffer=[5]
#line = sys.stdin.read()
#buffer.append(line)


newin = os.fdopen(sys.stdin.fileno(), 'r', 5)
i = 0
while i<10:
	kek = newin.read(5)
	print kek
	i = i + 1

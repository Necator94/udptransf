import sys
import io
import struct
import os

a = 'abcdef'

b = input('chislo:  ')
print b, '-number', bin(b), '-binNumber'
binNumber = bin(b)
n = binNumber[2:]
window = 9

c = n + a 

print c, '-str'

lenb = len(n)
print (lenb), ' - length of number'


while lenb  < window :
	c = '0' + c
	lenb = lenb +1
print c, 'result'


q = '11'
w = '0b00011'
q1 = int(q,2)
w1 = int(w,2)

if q1 == w1 :
	print 'kek' 

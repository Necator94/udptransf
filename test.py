import sys
import io


#f=open('kek.txt','r')
#ks=f.read();
#print ks

reader = io.open(sys.stdin.fileno())
print reader

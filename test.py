import sys
import io
import struct
import os


newin = os.fdopen(sys.stdin.fileno(), 'r' )

kek = newin.read(6)
print kek


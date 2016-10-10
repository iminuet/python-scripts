#!/usr/bin/env python
"""
Swap the bytes endian except for PBI CRC
2016-10-9: Add this script

Usage:
    ./byte_swap.py <file_name> <byte>
"""
import sys

try:
    file_name = sys.argv[1]
    byte = int(sys.argv[2])
except:
    print("Usage: ./byte_swap.py <file_name> <byte>")
    print("eg: ./byte_swap.py rcw_1600.bin 8\n")
    exit

with open(file_name,'rb') as file:
    tmp = file.read()
file.close()

with open(file_name + '.swap','wb') as file:
    for i in range(0, len(tmp) - 1, byte):
    	if(tmp[i:i+4].encode('hex')) == "08610040":
    		#print("PBI CRC command")
    		file.write(tmp[i:i+8])
    		break
	file.write(tmp[i:i+byte][::-1])
print("Swapped file: " + file_name + '.swap')
file.close()

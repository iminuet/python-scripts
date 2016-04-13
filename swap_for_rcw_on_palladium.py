#!/usr/bin/env python
#import os, re
count = 0
#my_list = []
#matches = []
print("opening uboot.bin.dat:..\n")

try:
	source = open("./uboot.bin.dat")
	line = source.readlines()
	source.close()
	if line[0] == '\n':
		del line[0]
	file_len = len(line)
	while count < file_len:
		each_line = line[count]
		del line[count]
		line.insert(count + 1, each_line)
		count += 2

	count = 0
	while count < file_len:
		each_line = line[count]
		each_line = each_line[(each_line.find(' ') + 1):]
		#debug
		#print each_line
		line[count] = each_line.lower()
		count += 1

	source = open("./uboot.bin.dat","w+")
	try:
		source.writelines(line)
	except:
		print("file write error!")
	source.close()
except:
	print("open file failed!\n")

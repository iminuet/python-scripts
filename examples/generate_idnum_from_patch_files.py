#!/usr/bin/env python
import sys,re
#git format-patch --numbered-files --start-number=10001
#using start number is 10001
#
#The result is in "commit_patch.txt". Format like:
#10001 b352dde
#10002 b310792
#10003 38e5a5a
#10004 2509814
#10005 5b782e3
#...
num = 10001;
print("opened file is commit_patch.txt\n")
inputnum = input("Enter the last file's number(should > 10001):")
f = open("commit_patch.txt", "w+")#only save one line!!
for num in range(10001, inputnum):
	try:
		in_file = open(str(num)) ##So the patch files are in current directory.
		line = in_file.readline()     #just read the first line
		list = re.findall(r'(.{4})',line)
		if list[0] == "From":
			f.write(str(num) + list[1] + list[2]+"\n")
		in_file.close()
	except:
		#pass
		print("file " + str(num) + " not exits")

#def search(str, list)
#	for i in range(1, len(list))
#		if list[i] == str:
#			id = list[i-1]
#		i = i + 4
#	return id

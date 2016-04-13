#!/usr/bin/env python
import os, re
#File: sort_patch.py
#Author: gqy
count = 0
my_list = []
matches = []
print("openning ls1043a_only.txt:..\n")

try:
	source = open("ls1043a_only.txt")        #including all modified files' paths
	line = source.readlines()
	for each_line in line:
	#input("file_path:\n") #source.readline()#source.readlines()-->return a list
		print ("file is " + each_line)
		loginfo = os.popen("git log " + each_line).readlines()
	#for the file given, find its related commitIDs
		print ("related commitID: ")
	#why line is empty?becuase id_patch has nothing updated
		for each_log in loginfo:
			try:
				tmp = re.findall(r'(.{7})', each_log)
				if tmp[0] == "commit ":
					my_list.append(tmp[1])
					print (tmp[1] + " ")
			except:
				pass
	source.close()
except:
	print("open file failed!\n")
#remove the duplicated item in my_list
print list(set(my_list))
#1.put the id-num matches in a list called matches[]
strings = open("./commit_patch.txt").read()
matches.extend(re.split('[\ \n]', strings))     #use extend instead of append!!!
#2.begin to match commitID and patch number
pnum = []
print("The match file is: ")
for i in range(0, len(my_list)):
	for j in range(1, 1198):
		#print("list is " + my_list[i] + " and match is " + matches[j])
		if my_list[i] == matches[j]:
			pnum.append(matches[j- 1])
			print ("[" + matches[j- 1] + "]" + matches[j])
			continue
print ("\n")
#3.sort the patch number files--->no need to sort, it already is.
pnum.sort()
print("The sorted match files are:\n")
print pnum
#try:
#	os.system("git am " + patch)
#except:
#	print("git am error!")

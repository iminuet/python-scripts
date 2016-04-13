#!/usr/bin/env python
import os, re
count = 0
my_list = []
matches = []
print("openning ls1043a_only.txt:..\n")
source = open("ls1043a_only.txt")        #including all modified files' paths
#id_patch = open("file_commit.txt", "w+")   #including one file's log info
try:
	line = input("file_path:\n")
	#input("file_path:\n") #source.readline()#source.readlines()-->return a list
	print ("file is " + line)
	loginfo = os.popen("git log " + line).readlines()
	#id_patch.writelines(loginfo)
except:
	print("open file failed!\n")
source.close()
#id_patch.flush()
#id_patch.close()
#for the file given, find its related commitIDs
#id_patch = open("file_commit.txt")
#line = id_patch.readline()
#print line
print ("related commitID: ")
#why line is empty?becuase id_patch has nothing updated
for each_line in loginfo:
	try:
		tmp = re.findall(r'(.{7})', each_line)
		if tmp[0] == "commit ":
			my_list.append(tmp[1])
			print (tmp[1] + " ")
#(str, commitID) = line.split(" ",1)	
#	if str is "commit":
#		print str
	except:
		pass
#		print count
#id_patch.close()
#1.put the id-num matches in a list called matches[]
strings = open("./commit_patch.txt").read()
matches.extend(re.split('[\ \n]', strings))     #use extend instead of append!!!
#2.begin to match commitID and patch number
print("The match file is: ")
for i in range(0, len(my_list)):
	for j in range(1, 1198):
		#print("list is " + my_list[i] + " and match is " + matches[j])
		if my_list[i] == matches[j]:
			pnum = matches[j- 1]
			print ("[" + pnum + "]" + matches[j])
			continue
print ("\n")
#num = 10
#patch = str(num)
#try:
#	os.system("git am " + patch)
#except:
#	print("git am error!")

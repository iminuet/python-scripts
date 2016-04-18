#!/usr/bin/env python
import os,re
#File: search_strings_in_git_log.py
#Goal: Use this script to find specified strings in git log such as
#	" fman ", " nand " and kinds of IP blocks. Then it shows
#	the whole lines and the commit ids that are related to the string.
#
#Attention:
#	Need blankets before and after the string in case it gets
#	unexpected commits.
#
#Status:
#	Draft. Not work.
#
f_old = None
patch_content = []

string_name = raw_input("Enter the IP block name: ")

def get_commit_in_log_line(line):	#deal with one line at a time
	if line[:7] == "commit ":
		line = re.findall(r'(.{7})', line) #return every 6 chars
		print(line[1] + "\n")

def get_commit_in_patch_line(in_file):
	line = in_file.readline()     #just read the first line
	my_line = re.findall(r'(.{4})', line) #return every 4 chars
	if my_line[0] == "From":
		#Commit ID should be at least 6 chars
		f.write(my_line[1] + my_line[2]+ "\n")
	return

#for each_new_file in new_patchset:
try:
	loginfo = os.popen("git log").readlines()
	for i in range(0, 10):
		get_commit_in_log_line(loginfo[i])

	count = 1
	new_flag = 0
	message_line_num = 0
	print("===============================================================")

except:
	#pass
	print("Error!")

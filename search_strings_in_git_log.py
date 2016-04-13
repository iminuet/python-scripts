#!/usr/bin/env python
import os
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

for each_new_file in new_patchset:
	try:
		loginfo = os.popen("git log -p").readlines()
		if loginfo.find(" " + string_name + " ")
				
		count = 1
		new_flag = 0
		message_line_num = 0
		print("===============================================================")
		
		f.close()
	except:
		#pass
		print("Error!")

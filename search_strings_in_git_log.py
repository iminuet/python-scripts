#!/usr/bin/env python
import os, re, time
#File: search_strings_in_git_log.py
#Goal: Use this script to find specified strings in git log such as
#    " fman ", " nand " and kinds of IP blocks. Then it shows
#    the whole lines and the commit ids that are related to the string.
#
#Attention:
#    Need blankets before and after the string in case it gets
#    unexpected commits.
#
#Status:
#    Could work a bit.
#

#keep track of the line numbers of current commit and next commit 
cur_commit_line = 0
next_commit_line = 0
#write the result to a new file named by the date:
ISOTIMEFORMAT='%Y-%m-%d-%H-%M-%S'
statistics_file = open(str(time.strftime(ISOTIMEFORMAT)), "w+")

def get_commit_in_log_line(line):    #deal with one line at a time
    if line[:7] == "commit ":
        #line = re.findall(r'(.{7})', line) #return every 6 chars
        return (str(line[7:14]))#else it returns "None".

def get_commit_in_patch_line(in_file):
    line = in_file.readline()     #just read the first line
    my_line = re.findall(r'(.{4})', line) #return every 4 chars
    if my_line[0] == "From":
        #Commit ID should be at least 6 chars
        f.write(my_line[1] + my_line[2]+ "\n")
    return

def search_strings_in_log(log, key):#(string0,*argv):
    for i in range(len(log) - 1, 0, -1):#!!#search from the bottom of the log
        if log[i].find(key) > 0: #!!#if no that key,return -1;##########
	    print(log[i])
            for j in range(0, 20):#20*2 is an assumed length of one log
                if log[i - j][:7] == "commit ":
                    cur_commit_line =  i - j
                    cur_commit_id = get_commit_in_log_line(log[cur_commit_line])
                    i = cur_commit_line
                    statistics_file.write(cur_commit_id + "|" + key +"|\n")
		    break
	elif i == 0:
            print(" Search to TOP of the file!")
    return 

#for each_new_file in new_patchset:
try:
    string_name = raw_input("Enter the IP block name: ")
    print("==========================================================")
    #Need to modify
    lognum = 50
    loginfo = os.popen("git log -" + str(lognum)).readlines()
    search_strings_in_log(loginfo, string_name)


    print("==========================================================")
except:
    #pass
    print("Main Error!")

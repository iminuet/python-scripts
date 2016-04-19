#!/usr/bin/env python
import os,re
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
#    Draft. Not work.
#
f_old = None
patch_content = []
#keep track of the line numbers of current commit and next commit 
cur_commit = 0
next_commit = 0

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
    for i in range(0, len(log)):#40 is the max length of the log
        if log[i].find(key) > 0: ####if no that key,return -1;##########
            print(log[i])
            for j in range(0, 20):#20*2 is an assumed length of one log
                if loginfo[i + j][:7] == "commit ":
                    next_commit =  i + j
                    print get_commit_in_log_line(loginfo[next_commit])
                    i = next_commit
                    break
    return 

#for each_new_file in new_patchset:
try:
    #Need to modify
    lognum = 4
    loginfo = os.popen("git log -" + str(lognum)).readlines()


    string_name = raw_input("Enter the IP block name: ")
    search_strings_in_log(loginfo, string_name)

    count = 1
    new_flag = 0
    message_line_num = 0
    print("==========================================================")
except:
    #pass
    print("Error!")

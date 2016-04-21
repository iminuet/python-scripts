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

lognum = 29
#keep track of the line numbers of current commit and next commit 
cur_commit_line = 0
next_commit_line = 0
#Need the generated file as the input:
commit_file = open("ls1046_upstream_patch_preparing/commit_patch.txt",\
"r").readlines()
#write the result to a new file named by the date:
ISOTIMEFORMAT='%Y-%m-%d-%H-%M-%S'
stat_file = open(str(time.strftime(ISOTIMEFORMAT)), "w+")
write_count = 0

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

def search_strings_in_log(log, key):#(list,*argv):
    for i in range(len(log) - 1, 0, -1):#!!#search from the bottom of the log
        if log[i].upper().find(key.upper()) > 0: #!!#if no that key,return -1;##########
            print(log[i])
            for j in range(0, 20):#20*2 is an assumed length of one log
                if log[i - j][:7] == "commit ":
                    cur_commit_line =  i - j
                    cur_commit_id = get_commit_in_log_line(log[cur_commit_line])
                    i = cur_commit_line
                    #print(cur_commit_id)
                    mark_ip_in_stat(cur_commit_id, key)
                    break
        elif i == 1:
            print("[Search to TOP of the file!]")
    return 

def mark_ip_in_stat(commit_id, ip_key):
    global write_count
    #range includes (len(commit_file) - 1) itself
    for i in range(write_count, len(commit_file) - 1):
	# if len(commit_file) = 29, then 0 ~ 28 is enough
        #print(str(i))
        each_line_list = commit_file[i].split(' ')
        #print(each_line_list)
        ##['10021', '764c05a\n'] or
        ##['10021', '764c05a', 'QSPI\n'] or
        ##['10021', '764c05a', 'QSPI,IFC\n']
        if each_line_list[1][:7] == commit_id:
            if len(each_line_list) < 3:
                commit_file[i] = commit_file[i][:-1] + " " +\
		ip_key + "\n"
            #elif each_line_list[2].find(',') == -1:
            else:
                commit_file[i] = commit_file[i][:-1] + "," +\
		ip_key + "\n"
            #debug
            #commit_file[i] = ("").join(each_line_list)
            #stat_file.write(commit_file[i])
            print(commit_file[i])
	    write_count = i + 1
	    break
    return
#for each_new_file in new_patchset:
try:
    loginfo = os.popen("git log -" + str(lognum)).readlines()
    #string_name = raw_input("Enter the IP block name: ")
    try:
        string_name = open("ip_list.txt","r").readlines()
    except:
	print("ip_list.txt open Error!")
    print("==========================================================")
    for i in range(0, len(string_name) - 1):
	if string_name[i] != '\n\n' and string_name[i][0] != '#':
            #debug
	    print(string_name[i])
            search_strings_in_log(loginfo, string_name[i].strip())
    print("==========================================================")
    stat_file.writelines(commit_file)
    stat_file.close()
except:
    #pass
    print("Main Error!")

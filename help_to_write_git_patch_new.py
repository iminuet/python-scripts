#!/usr/bin/env python
import os
#File: help_to_write_git_patch.py
#Goal: Help us to write the patch version message for git send-email
#      to upstream patchset more convenient
#
#Attention:
#    Only use this script when your patch version is >= V3, 
#    because for V2 version patchset there is no old change log to
#    get from V1 version patchset.
#
f_old = None
patch_content = []
old_patchset = []
new_patchset = []

print("Do you run checkpatch.pl first??\n")
#Please enter like: 10_22/
old_patchset_path = raw_input('''Enter the directory \
path of your old version \
patchset(eg.v2_my_patch/):''')
#Please enter like: 10_26/
new_patchset_path = raw_input("Enter the directory \
path of your new version \
patchset(eg.v3_my_patch/):")
#new_patchset = os.listdir(os.getcwd()) 
#Patches should be under the current director
new_patchset = os.listdir(new_patchset_path)
old_patchset = os.listdir(old_patchset_path)
new_patchset.sort()

#1.  To match the old patch(if exists) with the new modified patch file.
#    And deal with new added patches or deleted patches.
#2.  To port the old version messages to the new patchset
#3.  To enter the new version messages
for each_new_file in new_patchset:
    try:
        new_flag = 0
        message_line_num = 0
        if each_new_file == 'help_to_write_git_patch.py':
            continue
        if each_new_file[:4] == '0000':
            continue
#1. To match the old patch(if exists) with the new modified patch file.
#   And deal with new added patches or deleted patches.
        print('=========================================================')
        print(new_patchset_path + each_new_file)
        #print(os.getcwd() + old_patchset_path + each_new_file)
        print('=========================================================')
        
        try:
            #each_name_split is a list: ['0001','add-ls1043a-support.patch']
            f = open(new_patchset_path + each_new_file)
            patch_content = f.readlines()
            f.close()
        except:
            print("Cannot find the matched files! Check file name please!")
            break
    
        each_name_split = each_new_file.split('-', 1)
    
        for each_old_file in old_patchset:
            temp_string = each_old_file.split('-', 1)
            if temp_string[1] == each_name_split[1]:
                f_old = open(old_patchset_path + each_old_file)
                break
            f_old = None
        
        try:
            begin_line_num = patch_content.index('---\n')
        except:
            print("New Patch format error!")
            break

        count = 1
        if f_old == None:
            print("[New patch]\n")
            new_flag = 1
            patch_content.insert(begin_line_num + 1, " - New Patch.\n")
#2. To port the old version messages to the new version patchset
        else:
            old_patch_content = f_old.readlines()
            f_old.close()
            try:
                old_begin_line_num = old_patch_content.index('---\n')
            except:
                print("Old Patch format error!")
                break
            #If the old patch has change messages in it:
	    if old_patch_content[old_begin_line_num + 1][-2:] == ':\n':
                print("Porting version changes to the new patch..")

        	old_version = old_patch_content[3][17]
		if patch_content[begin_line_num + 1][0] == 'v':
        	    if patch_content[begin_line_num + 1][1] == str(old_version):
			    print("[Warning]: already ported the old messages!")
		else:
                    while True:
                        patch_content.insert(begin_line_num + count, \
                            old_patch_content[old_begin_line_num + count])
                        if old_patch_content[old_begin_line_num + count] == "\n":
                            break;
                        count += 1
            else:
                patch_content.insert(begin_line_num + 1,"\n")
                print("[Warning]:Old patch change log not found! Please confirm!\n" )
#3. To enter the new version messages
        print("Modifying.." + patch_content[3])
        version = patch_content[3][17]
        print("version is v" + version)
        #print("begin_line is " + str(begin_line_num))

	if patch_content[begin_line_num + 1][0] == 'v':
            if patch_content[begin_line_num + 1][1] == str(version):
		exists_flag = 1
                user = raw_input("There are already messages for the patch!\n\
                        A.Overwrite\nB.Print\nC.Quit\n")
                if user == "A":
                    while True:
                        if patch_content[begin_line_num + 2] == "\n":
                            del patch_content[begin_line_num + 2]
                            break
                        del patch_content[begin_line_num + 2]
                elif user == "B":
		    print_count = 0    
                    while True:
                        if patch_content[begin_line_num + print_count + 2] == "\n":
                            break
                        print patch_content[begin_line_num + print_count + 2]
			print_count += 1
                elif user == "C":
                    break
            else:
		exists_flag = 0
                patch_content.insert(begin_line_num + 1, "v" + version + ":\n")
        else:
	    exists_flag = 0
            patch_content.insert(begin_line_num + 1, "v" + version + ":\n")
        
        #Please use raw_input() instead of input()! input() only recognizes
	    #strings with "" ?!
        #If you want input() to recognize bit letter, you should use as "N".
        user = raw_input("Any changes for this patch?[Y/N/QUIT]\n")
        #debug
        if user.upper() == "N":
            if exists_flag == 0 and new_flag == 0:
                #The formal version is already no change, merge them together.
                if patch_content[begin_line_num + 3] == " - No change.\n":
                    del patch_content[begin_line_num + 1]
                    start_version = patch_content[begin_line_num + 1][1]
                    del patch_content[begin_line_num + 1]
                    patch_content.insert(begin_line_num + 1, "v" + \
				    start_version + "-v" + version + ":\n")
                else:
                    patch_content.insert(begin_line_num + 2, " - No change.\n")
	    elif new_flag == 1:#It's a NEW patch
                patch_content.insert(begin_line_num + 3, "\n")
        elif user.upper() == "QUIT":
            break
        else:
            while True:
                try:
                    if  user.upper() == "Y":
                        message_line = raw_input("Please enter the No."\
                            + str(message_line_num + 1) + \
                            " change messages:(better no more than 60 chars)\n")
                        patch_content.insert(begin_line_num + 2 + message_line_num,\
                            " - " + message_line + "\n")
                        message_line_num += 1

                        user = raw_input("More changes for this patch?\
					[Y/N/QUIT]\n")
                    else:
                        # No need blank line.
                        #patch_content.insert(begin_line_num + 2 +message_line_num,"\n")
                        break
                except:
                    print("Insert message error!")
        
        #print(patch_content[begin_line_num + 1 + message_line_num])
        #print(patch_content[begin_line_num + 2 + message_line_num])
        ## !!! Using "w+" will clear the file content immediately!!!!!!
        f = open(new_patchset_path + each_new_file, "w+")
        try:
            f.writelines(patch_content)
        except:
            print("file write error!")
            break
        f.close()
#4. To deal with cover letter patch!
#	try:
#	    cover = open(new_patchset_path + "0000-cover-letter.patch")
#	except:
#	    print("there is no cover letter patch!")
#	cover_content = cover.readlines()
#	cover.close()

    except:
        #pass
        print("Error!")

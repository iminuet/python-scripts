#!/usr/bin/env python
import os, re, time
#File: mark_patches_between_trees.py
#Goal: Mark if a patch is merged in a tree(SDK or Upsteam, eg.) or not.
#     
#""" diff file1 """
#	""" diff num1 """
#	""" diff body1 """
#		"""add or drop"""
#	""" diff num2 """
#	""" diff body2 """
#...
#""" diff file2 """
#	""" diff num1 """
#	""" diff body1 """
#...
#
#Attention:
#
error_code = [0, 1, 2, 3, 4]
#0: new patch to this git tree branch
#1: context differ or similiar, not apply
#2: existing already, not apply
#3: content differ, not apply
#4: no such context, not apply
#
""" [Function] will pick up usefull variables from only one line/string."""
""" [return value] The old and new line numbers' set, in total 4 numbers. """
def get_diff_num(line_string):#one of diff_num_lines[]
	""" The diff format(united): """
	""" @@ -old_num,old_count +new_num,new_count @@ """
	diff_num = []
	#find the old_num, old_count,new_num,new_count
	diff_num = re.findall(r"\d+\.?\d*",line_string)
	return diff_num

""" [Function] will pick up diff files'path from only one line/string."""
""" [return value] return one file's path a time """
def get_diff_file(line_string):#one of diff_file_lines[]
	""" The diff format(united) is like: """
	""" +++ b/board/freescale/ls1043ardb/cpld.c """
	""" No space is the first char """
	diff_file = line_string[6:]
	print(diff_file)
	return diff_file.strip('\n')

def get_diff_body(patch_file, start, end): #start/end pos in the patch file
	add_lines = []
	drop_lines = []
	unchange_lines = []
	#start line begins with "@@", so ignore it.
	for i in range(start + 1, end):
		if patch_file[i][0] == '+':
			if patch_file[i][1] != '+':#if not begins with "+++"
				add_lines.append(patch_file[i][1:])
		elif patch_file[i][0] == '-':
			if patch_file[i][1] != '-':#if not begins with "---"
				drop_lines.append(patch_file[i][1:])
		else:
			unchange_lines.append(patch_file[i])
	print("add_lines:")
	print(add_lines)
	print("drop_lines:")
	print(drop_lines)
	print("unchange_lines:")
	print(unchange_lines)

	return (add_lines, drop_lines, unchange_lines)

def get_commit_from_patch(patch_file):
    f = open(patch_file)
    line = f.readline()#just read the first line
    f.close()
    my_line = re.findall(r'(.{4})', line) #return every 4 chars
    if my_line[0] == "From":
        #Commit ID should be at least 6 chars
        commit_id = my_line[1] + my_line[2]
    	#print("Patch commit: " + commit_id)
    return commit_id.strip(' ')

def find_diff_nums_in_patch(patch_file):
	""" The diff format(united): """
	""" @@ -old_num,old_count +new_num,new_count @@ """
	f = open(patch_file)
	line = f.readlines()
	f.close()
	diff_num_lines = []
	diff_num_lines_num = []
	for i in range(0, len(line)):
		if line[i].find('@@ -') != -1:
			#diff_num_lines[0] is the line number
			diff_num_lines_num.append(i)
			diff_num_lines.append(line[i])
	return (diff_num_lines, diff_num_lines_num)

def find_diff_files_in_patch(patch_file):
	""" The diff format(united) is like: """
	""" +++ b/board/freescale/ls1043ardb/cpld.c """
	f = open(patch_file)
	line = f.readlines()
	f.close()
	diff_file_lines = []
	diff_file_lines_num = []
	for i in range(0, len(line)):
		if line[i].find('+++ b/') != -1:
			#diff_file_lines[0] is the line number
			diff_file_lines_num.append(i)
			diff_file_lines.append(line[i])
	return (diff_file_lines, diff_file_lines_num)

def compare_diff_lines_with_file(diff_num, add_lines, drop_lines, current_file):
	#diff_num is a list, contains [0]old_num, [1]old_count, [2]new_num,[3]new_count
	#diff_body has N lines, add_lines + drop_lines + unchange_lines
	# N = old_num + 2new_num - add_lines_num
	old_num = diff_num[0]
	old_count = diff_num[1]
	new_num = diff_num[2]
	new_count = diff_num[3]
	try:
		f = open(current_file)
		#file_lines = f.readlines()[90: 97]
		#file_lines = f.readlines(new_num + new_count)[new_num : new_num + new_count]
		file_lines = f.readlines()[new_num : new_num + new_count]
		f.close()
	except:
		print(" cannot find file in compare_diff_lines_with_file()\n")
	#print("Compared file part: ")
	#print(file_lines)
	
	""" Core Comparision Algorithm """
	#set(l1).issubset(set(l2))
	if set(add_lines).issubset(set(file_lines)) == True: 
	#if cmp(file_lines, diff_body) == 0:
		print(set(drop_lines) & set(file_lines))
		if set(drop_lines) & set(file_lines) == set([]):
			print("totally the same\n")
			error_code = 0
		else:
			print("NOT same: lines not drop")
			error_code = 2
	else:
		print("NOT same: no added lines\n")
		error_code = 1

	return error_code

#main function
patchset = []

#path = "/home/gqy/stash/ls1046a-uboot/ls1046a_patch_list_test/"
path = "./v_test_python/"

patchset = os.listdir(path)
patchset.sort()

ISOTIMEFORMAT='%Y-%m-%d-%H-%M-%S'
stat_file = open(str(time.strftime(ISOTIMEFORMAT)), "w+")
for each_file in patchset:
	diff_num_lines = []
	diff_num_lines_num = []
	diff_num = []
	diff_file_lines = []
	diff_file_lines_num = []

	commit_id = get_commit_from_patch(path + each_file)
	print(path + each_file)
    	print("Patch commit: " + commit_id)
	f = open(path + each_file, "r")
	patch_content = f.readlines()
	f.close()

	(diff_num_lines, diff_num_lines_num) = find_diff_nums_in_patch(path + each_file)
	(diff_file_lines, diff_file_lines_num) = find_diff_files_in_patch(path + each_file)
	print("diff file set: ") 
	print(diff_file_lines)
	print("diff file line num: ")
	print(diff_file_lines_num)
	print("diff num set: ")
	print(diff_num_lines)
	print("diff num line num: ")
	print(diff_num_lines_num)
	count_num = 0
	error_code = 0
	stat_file.writelines(commit_id + "" + path + each_file + "\n")
	for i in range(0, len(diff_file_lines)):
		if error_code != 0:
			break
		diff_file = get_diff_file(diff_file_lines[i])
		print("diff file is: ")
		print(diff_file)
		try:
			f = open(diff_file)#should under u-boot direcory
			f.close()
		except:
			print("cannot find " + diff_file + "under current dir!")
			stat_file.writelines("ERROR: no such a file!" + diff_file + "\n")
			continue
		try:
			if i != len(diff_file_lines_num) - 1:
				#if j is not the last element of the list.
				print("Not the last file: ")
				next_file_line_num = diff_file_lines_num[i + 1]
			else:
			#At the end of a patch file, there are three more unrelavent lines.
				print("It's the last file: ")
				next_file_line_num = len(patch_content) - 3
		except:
			print("next_file_line_num met error!")
			pass
		for j in range(count_num, len(diff_num_lines_num)):
			each_num = diff_num_lines_num[j]
			if each_num < i:
				continue
			if j != len(diff_num_lines_num) - 1:
				#if j is not the last element of the list.
				print("Not the last num: ")
				next_num = diff_num_lines_num[j + 1]
			else:
			#At the end of a patch file, there are three more unrelavent lines.
				print("It's the last num: ")
				next_num = len(patch_content) - 3
			""" each_num will indicate a comparision of diff&files"""
			try:
			#diff_file_lines[i + 1] must < len(diff_file)
			#	if i == len(diff_file_lines) - 1:
			#		continue
			#	if diff_file_lines_num[i + 1] >= len(patch_content) - 1:
			#		print("diff_file_lines[i + 1] must < \
			#			len(patch_file)")
			#		continue
				print("removed this exception...")
			except:
				pass

			if each_num < next_file_line_num:
				diff_num = \
				get_diff_num(diff_num_lines[j])
				print("diff num: ")
				print(diff_num)
				diff_num = diff_num[:4]
				#Use 'map' to convert strings to integars
				diff_num = map(int, diff_num)
				
				print("next line num is?")
				print(next_file_line_num)
				print(next_num)
				(add_lines, drop_lines, unchange_lines) = \
						get_diff_body(patch_content, \
						each_num, \
						min(next_file_line_num, \
						next_num))
				diff_body = add_lines + unchange_lines 

				error_code = \
				compare_diff_lines_with_file(diff_num, \
				add_lines, drop_lines, diff_file)
				print(str(error_code))
				#stat_file.writelines(" "+ diff_file + "\n")
				if error_code != 0:
					stat_file.writelines(str(error_code) + "\n")
					break
			else:
				count_num = j;
				continue
				
stat_file.close()

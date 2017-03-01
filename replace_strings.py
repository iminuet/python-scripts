#!/usr/bin/env python
import os

my_files = []
subfiles = []
#######################path = "configs/"
path="./"
""" Only current path """
all_files = os.listdir(path)
""" Pick out the specific files whose names begin with 'ls1046a' """
for each_file in all_files:
	if each_file[:7] == 'ls1046a' or each_file[:7] == 'ls1043a' or each_file[:7] == 'lsqqqqa':
		my_files.insert(0, each_file)
##Add new here##		

for each_file in my_files:
	""" All paths/subdirecories"""
	if 1:
		subfiles = os.popen("find " + each_file + " -name '*.rcw'").readlines()
	for rcw_file in subfiles:
		#rcw_file[] format is like:
		# "ls1046ardb_intpsr/RR_SSPH_3358/rcw_1600_qspiboot.rcw\n"
		if rcw_file[-5:] == ".rcw\n" and rcw_file.find("qspiboot") != -1:
			rp = open(rcw_file.strip())
			rtmp = rp.readlines()
			rp.close()
			rtmp.append(".pbi\nwrite 0x550000, 0x000f400c\n.end\n")
			##Add new here##		
			##Add new here##		
			rp = open(rcw_file.strip(), "w+")
			rp.writelines(rtmp)
			rp.close()
	if os.path.isdir(each_file): 
		print(each_file + " is a dir")
		exit
	try: 
		fp = open(path + each_file)
		tmp = fp.readlines()
		fp.close()
		"""A. Replace the specific string '1043' in those specific files"""
	#	for num in range(0, len(tmp)):
	#		tmp[num] = tmp[num].replace('1043', '1046')
		"""B. Delete specific lines that contain the string 'CONFIG_FSL_LSCH' """
		tmp2 = [] # new blanket list
		for each_line in tmp:
		       if each_line.find('#define CONFIG_FSL_LAYERSCAPE') == -1:
			if each_line.find('#define CONFIG_FSL_LSCH') == -1:
			 if each_line.find('#define CONFIG_LS1043A') == -1:
			  if each_line.find('#define CONFIG_LS1012A') == -1:
			   if each_line.find('#define CONFIG_LS2080A') == -1:
			     tmp2.append(each_line)
		"""C. Insert a string in the second line: CONFIG_FSL_LAYERSCAPE=y """
	#	print(tmp[1])
	#	if tmp[1] != "CONFIG_FSL_LAYERSCAPE=y\n":
	#		tmp.insert(1, "CONFIG_FSL_LAYERSCAPE=y\n")

		fp = open(path + each_file, "w+")
		fp.writelines(tmp2)
	#	
		fp = open(path + each_file, "w+")
		#fp.writelines(tmp)
		fp.close()
	except:
		exit


#!/usr/bin/env python
import os,sys
# Goal:
# This script is just for building uboot for LS platforms.
# And copy the image to specific NXP servers.
#
# Usage:
# ./make_uboot.py <defconfig_name> (<server_name>) #TITAN is default
#
my_dict = {"gqy":"b52263", "hmk":"b21284", "hzq":"b48286", "swb":"b53747"}

local_user = os.popen("env|grep -e 'LOGNAME=' ").read().split('=')[1][:-1]
print("Default user: " + local_user)
print_info = []
# Tech Using Python modules:
# os.system(command): call shell commands but will return status code
# os.popen(command): call shell commands but use .read() to get the content
# sys.argv[0] is this script's name. len(sys.argv) contains script's name!
# os._exit(), sys.exit(),os.kill(..)
#
#
uboot_defconfig_path = "./configs/"
server_name = ''
# 1.Type the right defconfig
if len(sys.argv) < 2:
	print("ERROR: Please assign a defconfig to build!\n")
	print("[Usage]:")
	print(" ./make_uboot.py <defconfig_name> (<server_name>)")
	print("""- server options: titan, star/boardfarm, rhuath, \
palladium/emulator.\n""")
	os._exit()
defconfig_name = sys.argv[1]
print("get defconifg: " + defconfig_name)

uboot_defconfigs = os.listdir(uboot_defconfig_path)
#The next line would get system error if the defconfig is not correct!
uboot_defconfigs.index(defconfig_name)

# NOTE: 'defconfig_name' should be '<board_name>_<boot_method>_defconfig',
# for example: ls1043aqds_sdcard_qspi_defconfig
if len(sys.argv) == 3:#NOTE: so here should be 3!
	server_name = sys.argv[2]
	print("get server's name: " + server_name)
# 2.Build U-Boot
os.system("make " + defconfig_name)
os.system("make -j22")
print("Compile done! ..\n")
# 3.Copy U-Boot to server
board_name = defconfig_name.split('_')[0]
boot_method = defconfig_name.split('_')[1]
if server_name == '' or server_name.lower() == 'titan':
	#titan is default local server, so no need remote_flag or ip_addr
	remote_flag = ''
	#ERROR:
	#Traceback (most recent call last):
	#File "./make_uboot.py", line 47, in <module>
	#      user = os.system("env|grep -e 'LOGNAME=' ").split('=')[1]
	#      AttributeError: 'int' object has no attribute 'split'
	rev_dict = dict((v,k) for k,v in my_dict.items())
	if rev_dict.has_key(local_user):
		user = rev_dict[local_user]
		remote_flag = 's'
		ip_addr = '10.192.208.233'
	else:
		user = local_user #Name
		ip_addr = ''
elif server_name.lower() == 'rhuath':
	if my_dict.has_key(local_user):
		user = my_dict[local_user]
		remote_flag = 's'
		ip_addr = user + '@10.81.117.101:'
		print("Change to remote user: " + user)
	else:
		user = local_user #CoreID
		ip_addr = ''
elif server_name.lower() == 'star' or  server_name.lower() == 'boardfarm':
	if my_dict.has_key(local_user):
		user = my_dict[local_user]
		remote_flag = 's'
		ip_addr = user + '@10.192.208.10:'
		print("Change to remote user: " + user)
	else:
		user = local_user #CoreID
		ip_addr = ''
elif server_name.lower() == 'emulator' or  server_name.lower() == 'palladium':
	if my_dict.has_key(local_user):
		user = my_dict[local_user]
		remote_flag = 's'
		ip_addr = user + '@10.112.101.66:'
		print("Change to remote user: " + user)
	else:
		user = local_user #CoreID
		ip_addr = ''

try:
	if boot_method == "sdcard":
		boot_name = "SD"
		rcw_image = ""
		uboot_image = 'u-boot-with-spl-pbl.bin'
		if defconfig_name.split('_')[2] == "qspi":
			support = "qspi"
		else:
			support = ""
	elif boot_method == "nand":
		boot_name = "NAND"
		rcw_image = ""
		uboot_image = 'u-boot-with-spl-pbl.bin'
		support = ""
	elif boot_method == "qspi":
		boot_name = "QSPI"
		os.system("tclsh byte_swap.tcl u-boot-dtb.bin u-boot_swap.bin 8")	
		rcw_image = "rcw_qspi_1600_swap.bin"
		uboot_image = 'u-boot_swap.bin'
		support = ""
	else:#should be nor boot
		boot_name = "NOR"
		rcw_image = "rcw_1600.bin"
		uboot_image = 'u-boot-dtb.bin'
		support = ""

# NOTE: See if the board directory exists, go on; if not, create one.
	path = "/tftpboot/" + user + "/" + board_name + "/"
	local_path = "/tftpboot/" + local_user + "/" + board_name + "/"
	if not os.path.exists(local_path):
		print("creating a new directory at " + local_path)
       	#Create for local server
		os.mkdir(local_path)
       	#Create copies for remote server
	if user != local_user:
		print("Copy local directory " + local_path + " to " + ip_addr \
		+ path)
		os.system("scp -r --reply=yes " + local_path + " " + ip_addr \
		+ path)
except:
	print("Shell commands get problems on server!\n")

"""copy the u-boot image to /tftpboot/<user>/<board_name>/ """
print("Copy " + uboot_image + " to " + path)
os.system(remote_flag + "cp " + uboot_image + " " + ip_addr + path) 

#4. Print U-Boot commands to write rcw, U-Boot, Kernel image into boot device.
f = open("/home/gqy/python_scripts/u-boot/resources/boot_commands").readlines()
# NOTE: 'list' object has no attibute 'find'. Should use .index(). 
#       Only 'string' could use .find() to find a char or a sub string. 
for each_line in f:
	if each_line.find(boot_name) > 0:
		line_num = f.index(each_line)
#print("Begin from: " + f[line_num + 1])
tmp = 0
while f[line_num + tmp + 1][0] != '=':
	print_info.insert(tmp, f[line_num + tmp + 1])
	tmp = tmp + 1

#NOTE: Replace all the variables: <user_name>, <board_name>, <rcw_image>,
#<uboot_image>, <cpld_or_qixis_command>, <sd_or_sd_qspi>

if(board_name[-3:] == "qds"):
	cpld_or_qixis_command = "qixis_reset"
elif(board_name[-3:] == "rdb"):
	cpld_or_qixis_command = "cpld reset"
else:
	cpld_or_qixis_command = ""
	print("Unknown FPGA/CPLD type!")
if support == "qspi":
	sd_or_sd_qspi = "sd_qspi"
else:
	sd_or_sd_qspi = "sd"

for each_line in print_info:
#NOTE: replace won't affect the origin variable's value.
#So need to assign back to each_line.
	each_line = each_line.replace('<user_name>', user)
	each_line = each_line.replace('<board_name>', board_name)
	each_line = each_line.replace('<rcw_image>', rcw_image)
	each_line = each_line.replace('<uboot_image>', uboot_image)
	each_line = each_line.replace('<cpld_or_qixis_command>', cpld_or_qixis_command)
	each_line = each_line.replace('<sd_or_sd_qspi>', sd_or_sd_qspi)
#NOTE: Add ',' to let 'print' not add a newline!
	print(each_line),

#Print command to boot linux:
print(f[-2]),
f[-1] = f[-1].replace('<user_name>', user)
print(f[-1].replace('<board_name>', board_name))

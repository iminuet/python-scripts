#!/usr/bin/env python
import os,sys
# Goal:
# This script is just for building uboot for LS platforms.
# And copy the image to specific NXP servers.
#
# Usage:
# ./make_uboot.py <defconfig_name> (<server_name>) #TITAN is default
#
# Tech Using Python modules:
# os.system(command): call shell commands
# sys.argv[0] is this script's name. len(sys.argv) contains script's name!
# os._exit(), sys.exit(),os.kill(..)
#
#
uboot_defconfig_path = "./configs/"
server_name = ''
# 1.Type the right defconfig
if len(sys.argv) < 2:
	print("ERROR: Please assign a defconfig to build!\n")
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
print("Compile done! begin to copy to /tftpboot/gqy/..\n")
# 3.Copy U-Boot to server
board_name = defconfig_name.split('_')[0]
boot_method = defconfig_name.split('_')[1]
# NOTE: See if the board directory exists, go on; if not, create one.
if server_name == '' or server_name.lower() == 'titan':
	#titan is default local server, so no need remote_flag or ip_addr
	remote_flag = ''
	user = 'gqy'
	ip_addr = ''
elif server_name.lower() == 'rhuath':
	remote_flag = 's'
	user = 'B52263'
	ip_addr = 'B52263@10.81.117.101:'
elif server_name.lower() == 'star':
	remote_flag = 's'
	user = 'B52263'
	ip_addr = 'B52263@10.192.208.10:'
elif server_name.lower() == 'emulator' or  server_name.lower() == 'palladium':
	remote_flag = 's'
	user = 'B52263'
	ip_addr = 'B52263@10.112.101.66:'

try:
	if boot_method == "sdcard" or boot_method == "nand":
		image_name = 'u-boot-with-spl-pbl.bin'
	elif boot_method == "qspi":
		os.system("tclsh byte_swap.tcl u-boot-dtb.bin u-boot_swap.bin 8")	
		image_name = 'u-boot_swap.bin'
	else:#should be nor boot
		image_name = 'u-boot-dtb.bin'

	path = "/tftpboot/" + user + "/" + board_name
#	if not os.path.exists(path):
#		print("creating a new directory at " + path)
		#Create for remote server
#		os.mkdir(ip_addr + path)
except:
	print("Shell commands get problems on server!\n")

print("Copy " + image_name + " to " + path)
os.system(remote_flag + "cp " + image_name + " " + ip_addr + path) 












# python-scripts
byte_swap.py:

- Use to swap the bytes for NXP Layerscape Platform boards
 (LS1012A/LS1043A/LS1046A) because of the QSPI SoC errata. 

usage:
$./byte_swap.py <file_name> <byte>

==============================================================================
make_uboot.py

- Use to compile the supported boards' U-Boot image
  and copy the image to specific directory on specific local or remote server
  Supported boards are most NXP Layerscape Platform boards(QDS/RDB).

usage:

$./make_uboot.py <board_name>_<boot_method>_defconfig <server_name>

==============================================================================
help_to_write_git_patch_new.py 

- Use to push patches to upstream(opensource community).
  Could port the change logs from old version to new version of the same patchset.
  Could automatically add the change log for unchanged patches.
  Deal with the patches one by one in order.

note:
- Only need to use this script from version 3 patchset.

usage:

$./help_to_write_git_patch_new.py 

Enter the directory path of your old version patchset(eg.v2_my_patch/):~/tmp/opensource/u-boot/v2_my_patch/
Enter the directory path of your new version patchset(eg.v3_my_patch/):~/tmp/opensource/u-boot/v3_my_patch/

# python-scripts
byte_swap.py:

- Use to swap the bytes for NXP Layerscape Platform boards
 (LS1012A/LS1043A/LS1046A) because of the QSPI SoC errata. 

usage:
$./byte_swap.py <file_name> <byte>

==============================================================================
make_uboot.py

- Use to compile the supported boards' U-Boot image
  and copy the image to specific directory on specific server
  Supported boards are most NXP Layerscape Platform boards(QDS/RDB).

usage:

$./make_uboot.py <board_name>_<boot_method>_defconfig <server_name>

==============================================================================

An mtp responder written in python.

Uses configfs and functionfs.

Should now be fully functional.

Note

## How to set up a Raspberry Pi Zero to run it:

1. Create a regular Raspbian Lite SD card.

2. Touch `/boot/ssh` to enable ssh.

3. Edit `config.txt` and add this line to enable USB device mode:

       dtoverlay=dwc2

4. Edit `/etc/modules` and add this line to enable USB composite driver:

       libcomposite

5. Load the module manually one time (it will load automatically after
   a reboot):

       sudo modprobe libcomposite


## How to set up a PC to run it in loopback mode:

1. Kernel must have libcomposite and dummy_hcd.

   dummy_hcd is not available in Ubuntu. You can build it yourself
   using DKMS by following these steps:

   https://serianox.github.io/gadgetfs-ubuntu.html

   On Ubuntu 16.04 you need linux 4.4.0-100 or later to fix a bug when
   removing the gadget. Without the patch the kernel will crash.

   After you built and installed dummy_hcd, add to `/etc/modules`:

       dummy_hcd
       libcomposite

2. Load the modules manually one time (they will load automatically
   after a reboot):

       sudo modprobe dummy_hcd
       sudo modprobe libcomposite


## How to install it:

    pip3 install .


## How to run it:

    sudo ./pymtpd --udc <UDC>

   UDC should be `dummy_udc.0` if you are running on a PC, or
   `20980000.usb` if running on a Raspberry Pi Zero.

   It shares the contents of /tmp/mtp (which will be created on start
   up.)
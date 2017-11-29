An mtp responder written in python.

Uses configfs and functionfs.

Not functional yet.

How to use:

1. Kernel must have libcomposite and dummy_hcd.

   dummy_hcd is not available in Ubuntu. You can build it yourself
using DKMS by following these steps:

   https://serianox.github.io/gadgetfs-ubuntu.html

   On Ubuntu 16.04 you need linux 4.4.0-100 to fix a bug when removing
the gadget. Without the patch the kernel will crash.

   After you built and installed dummy_hcd, add to /etc/modules:

       dummy_hcd
       libcomposite

2. Python modules required: functionfs, construct, inotify-simple

   You can run these as regular user or root depending on where you
want them installed. It works either way. I recommend not using root
if you're just testing or developing.

       pip3 install functionfs
       pip3 install construct
       pip3 install inotify-simple

3. As root, run ./pymtpd

   It configures all the configfs stuff and mounts the functionfs.
Then it starts handling MTP requests.

4. Open your file manager and you should see an MTP device.

   It shares the contents of /tmp/mtp (which will be created on start
up.) Copy some files into the directory and they should show up in the
file manager immediately. It is not feature complete yet, but browsing
and fetching files should work.
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

2. As root, run configure.py

This creates the gadget configuration. It will wait forever. If you
interrupt it with ctrl-c, it will try to remove the gadget config.

It is also responsible for mounting the mtp functionfs.

3. As root, run ./pymtpd

4. As root, run mtp-detect from mtp-tools package.

You should see some output from pymtpd. mtp-detect will crash, because
pymtpd is not fully implemented yet.

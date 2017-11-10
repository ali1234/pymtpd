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

2. Python modules required: functionfs and construct.

You can run these as regular user or root depending on where you
want them installed. It works either way.

    pip3 install functionfs
    pip3 install construct

Note: functionfs does not support py3 yet, clone this repo:

    git clone -b pycompat git://github.com/ali1234/python-functionfs

and run this in the root of the repo:

    pip3 install .

3. As root, run ./pymtpd

It configures all the configfs stuff and mounts the functionfs.
Then it starts handling MTP requests.

4. As root, run mtp-detect from mtp-tools package.

You should see some output from pymtpd. mtp-detect will crash, because
pymtpd is not fully implemented yet.

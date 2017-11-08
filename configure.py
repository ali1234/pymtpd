#!/usr/bin/env python3

import os, stat, time, subprocess




class Directory(object):
    def __init__(self, path):
        object.__setattr__(self, 'path', path)

    def __setattr__(self, key, value):
        path = object.__getattribute__(self, 'path')
        if type(value) == str:
            with open(os.path.join(path, key), 'w') as k:
                k.write(value)
        elif type(value) == Directory:
            os.symlink(object.__getattribute__(value, 'path'), os.path.join(path, key))
        elif value is None:
            os.makedirs(os.path.join(path, key))

    def __getattribute__(self, key):
        path = object.__getattribute__(self, 'path')
        attr = os.path.join(path, key)
        try:
            mode = os.stat(attr)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                return Directory(attr)
            elif stat.S_ISREG(mode):
                with open(attr, 'r') as f:
                    value = f.read()
                return value
        except FileNotFoundError:
            return NotExist(attr)

    def __delattr__(self, key):
        path = object.__getattribute__(self, 'path')
        attr = os.path.join(path, key)
        mode = os.lstat(attr)[stat.ST_MODE]
        if stat.S_ISDIR(mode):
            os.rmdir(attr)
        else:
            os.unlink(attr)

    def __getitem__(self, key):
        return type(self).__getattribute__(self, key)

    def __setitem__(self, key, value):
        return type(self).__setattr__(self, key, value)

    def __delitem__(self, key):
        return type(self).__delattr__(self, key)


class NotExist(Directory):

    def __setattr__(self, key, value):
        path = object.__getattribute__(self, 'path')
        os.makedirs(path, exist_ok=True)
        Directory.__setattr__(self, key, value)




CONFIGDIR = '/sys/kernel/config/usb_gadget/'
#CONFIGDIR = '/tmp/cfs/'

class Gadget(object):
    def __init__(self, name, vid, pid):
        self.name = name
        self.vid = vid
        self.pid = pid
        self.gadget = Directory(CONFIGDIR)[self.name]

    def add_function_to_config(self, function, config):
        if type(self.gadget.functions[function]) == NotExist:
            self.gadget.functions[function] = None
        self.gadget.configs[config][function] = self.gadget.functions[function]

    def remove_function_from_config(self, function, config):
        del self.gadget.configs[config][function]

class PiratePython(Gadget):

    def __enter__(self):
        print('Configuring gadget')
        self.gadget.bcdUSB = '0x0200'
        self.gadget.bDeviceClass = '0x02'
        self.gadget.bDeviceSubClass = '0x02'
        self.gadget.bcdDevice = '0x3008'
        self.gadget.idVendor = self.vid
        self.gadget.idProduct = self.pid

        self.gadget.os_desc.use = '1'
        self.gadget.os_desc.b_vendor_code = '0xcd'
        self.gadget.os_desc.qw_sign = 'MSFT100'

        self.gadget.strings['0x409'].serialnumber = '9112473'
        self.gadget.strings['0x409'].manufacturer = 'Pimoroni Ltd.'
        self.gadget.strings['0x409'].product = 'PiratePython'

        self.gadget.functions['rndis.usb0'].os_desc['interface.rndis'].compatible_id = 'RNDIS'
        self.gadget.functions['rndis.usb0'].os_desc['interface.rndis'].sub_compatible_id = '5162001'

        self.gadget.configs['c.1'].strings['0x409'].configuration = 'mtp test'

        self.add_function_to_config('rndis.usb0', 'c.1')
        self.add_function_to_config('acm.GS0', 'c.1')
        self.add_function_to_config('acm.GS1', 'c.1')
        self.add_function_to_config('acm.GS2', 'c.1')
        self.add_function_to_config('acm.GS3', 'c.1')
        self.add_function_to_config('ffs.mtp', 'c.1')

        os.makedirs('/dev/mtp', exist_ok=True)
        subprocess.call(['mount', '-c', '-t', 'functionfs', 'mtp', '/dev/mtp'])

        return self

    def __exit__(self, t, value, traceback):
        print('Tearing down gadget')
        self.gadget.UDC = ''

        subprocess.call(['umount', '/dev/mtp'])

        self.remove_function_from_config('rndis.usb0', 'c.1')
        self.remove_function_from_config('acm.GS0', 'c.1')
        self.remove_function_from_config('acm.GS1', 'c.1')
        self.remove_function_from_config('acm.GS2', 'c.1')
        self.remove_function_from_config('acm.GS3', 'c.1')
        self.remove_function_from_config('ffs.mtp', 'c.1')

        del self.gadget.configs['c.1'].strings['0x409']
        del self.gadget.configs['c.1']
        del self.gadget.functions['rndis.usb0']
        del self.gadget.functions['acm.GS0']
        del self.gadget.functions['acm.GS1']
        del self.gadget.functions['acm.GS2']
        del self.gadget.functions['acm.GS3']
        del self.gadget.functions['ffs.mtp']
        del self.gadget.strings['0x409']

        del Directory(CONFIGDIR)[self.name]


class OutputRedirect(object):
    def __init__(self, dev):
        self.dev = dev

    def __enter__(self):
        self.oldfds = [os.dup(n) for n in range(3)]
        fd = os.open(self.dev, os.O_RDWR)
        [os.dup2(fd, n) for n in range(3)]
        os.close(fd)
        return self

    def __exit__(self, t, value, traceback):
        [os.dup2(self.oldfds[n], n) for n in range(3)]




if __name__ == '__main__':

    with PiratePython(name='g1', vid='0x0430', pid='0xa4a2') as p:
        #with OutputRedirect('/dev/ttyGS0') as o:

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Shutting down")

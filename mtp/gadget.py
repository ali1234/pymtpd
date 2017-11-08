import os, stat, time

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

    def bind(self, udc):
        self.gadget.UDC = udc

    def remove_gadget(self):
        del Directory(CONFIGDIR)[self.name]

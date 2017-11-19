import itertools
import pathlib
import logging
import os
logger = logging.getLogger(__name__)

from construct import *
from inotify_simple import INotify, flags
IN_MASK = flags.ATTRIB | flags.CREATE | flags.DELETE | flags.MODIFY | flags.MOVED_TO | flags.MOVED_FROM

import mtp.constants
from mtp.adapters import MTPString
from mtp.exceptions import MTPError
from mtp.object import Object




StorageType = Enum(Int16ul, **dict(mtp.constants.storage_types))
StorageFileSystems = Enum(Int16ul, **dict(mtp.constants.storage_file_systems))
StorageAccess = Enum(Int16ul, **dict(mtp.constants.storage_accesss))

StorageInfo = Struct(
    'storage_type' / Default(StorageType, 'FIXED_RAM'),
    'filesystem_type' / Default(StorageFileSystems, 'HIERARCHICAL'),
    'access_capability' / Default(StorageAccess, 'READ_WRITE'),
    'max_capacity' / Int64ul,
    'free_space' / Int64ul,
    'free_space_in_objects' / Default(Int32ul, 0xffffffff),
    'storage_description' / Default(MTPString, u''),
    'volume_identifier' / Default(MTPString, u''),
)


class Storage(object):

    counter = itertools.count(0x10001)

    def __init__(self, path, name, writable=False):
        self._id = next(self.counter)
        self._path = pathlib.Path(path)
        self.__name = name
        self.__writable = writable
        self.__objects = dict()

    def connect(self, intep, loop):
        logger.debug('Connect Storage: %x, %s, %s' % (self._id, self.__name, str(self._path)))
        self.__intep = intep
        self.__loop = loop
        self.__inotify = INotify()
        self.__watchfd = self.__inotify.add_watch(str(self._path), IN_MASK)
        self.__loop.add_reader(self.__inotify.fd, self.__inotify_event)
        self.dirscan(self._path)  # objects in root dir have no parent

    def __inotify_event(self):
        for event in self.__inotify.read():
            print(event)

    def disconnect(self):
        logger.debug('Disconnect Storage: %x, %s, %s' % (self._id, self.__name, str(self._path)))
        self.__loop.remove_reader(self.__fanfd)
        os.close(self.__fanfd)

    def dirscan(self, path, parent=None):
        for fz in path.iterdir():
            obj = Object(self, fz, parent)
            self.__objects[obj._handle] = obj
            if fz.is_dir():
                obj.__watchfd = self.__inotify.add_watch(str(fz), IN_MASK)
                self.dirscan(fz, obj)

    def build(self):
        return StorageInfo.build(dict(max_capacity=1000000000, free_space=100000000, volume_identifier=self.__name,
                                      storage_description=self.__name))

    def handles(self, parent=0):
        if parent == 0:
            return self.__objects.keys()
        elif parent == 0xffffffff:  # yes, the spec is really dumb
            return (k for k, v in self.__objects.items() if v._parent == None)
        else:
            try:
                p = self.__objects[parent]
            except KeyError:
                raise MTPError("INVALID_PARENT_OBJECT")
            else:
                return (k for k, v in self.__objects.items() if v._parent == p)

    def __getitem__(self, item):
        try:
            return self.__objects[item]
        except KeyError:
            raise MTPError('INVALID_OBJECT_HANDLE')


class StorageManager(object):

    def __init__(self, intep, loop, *stores):
        self.intep = intep
        self.loop = loop
        self.__stores = dict()
        for s in stores:
            self.__add(s)

    def ids(self):
        return self.__stores.keys()

    def handles(self, parent=0):
        return itertools.chain(s.handles(parent) for s in self.__stores.values())

    def object(self, handle):
        for s in self.__stores.values():
            try:
                return s[handle]
            except MTPError:
                continue
        raise MTPError('INVALID_OBJECT_HANDLE')

    def __add(self, store):
        self.__stores[store._id] = store
        store.connect(self.intep, self.loop)

    def add(self, store):
        self.__add(store)

    def __getitem__(self, key):
        try:
            return self.__stores[key]
        except KeyError:
            raise MTPError('STORE_NOT_AVAILABLE')

    def __delitem__(self, key):
        self.__stores[key].disconnect()
        del self.__stores[key]



if __name__ == '__main__':
    sm = StorageManager(
        ('/tmp/mtp', u'Files', True),
    )

    for k in sm.handles():
        print(k, StorageInfo.parse(sm[k].build()))

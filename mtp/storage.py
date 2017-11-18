import itertools
import pathlib
import logging
logger = logging.getLogger(__name__)

from construct import *

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

    def __init__(self, id, path, name, writable=False):
        self._id = id
        self._path = pathlib.Path(path)
        self.__name = name
        self.__writable = writable
        self.__objects = dict()
        logger.debug('Create Storage: %x, %s, %s' % (self._id, self.__name, str(self._path)))
        self.dirscan(self._path)  # objects in root dir have no parent

    def dirscan(self, path, parent=None):
        for fz in path.iterdir():
            obj = Object(self, fz, parent)
            self.__objects[obj._handle] = obj
            if fz.is_dir():
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

    def __init__(self, *args):
        self.__stores = dict()
        for n,arg in enumerate(args):
            storage_id = n+0x00010001
            self.__stores[storage_id] = Storage(storage_id, *arg)

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

    def __getitem__(self, key):
        try:
            return self.__stores[key]
        except KeyError:
            raise MTPError('STORE_NOT_AVAILABLE')




if __name__ == '__main__':
    sm = StorageManager(
        ('/tmp/mtp', u'Files', True),
    )

    for k in sm.handles():
        print(k, StorageInfo.parse(sm[k].build()))

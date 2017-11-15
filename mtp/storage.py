import itertools
import pathlib

from construct import *

import mtp.constants
from mtp.adapters import MTPString
from mtp.exceptions import MTPError
from mtp.properties import Properties
from mtp.object import ObjectManager


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




class StorageManager(Properties):
    class __Storage(object):
        keyerror = MTPError('STORE_NOT_AVAILABLE')

        def __init__(self, id, path, name, writable=False):
            self.__id = id
            self.__path = path
            self.__name = name
            self.__writable = writable
            self.__objects = ObjectManager()

            self.dirscan(pathlib.Path(self.__path), 0x0) # objects in root dir have parent=0

        def dirscan(self, path, parent_id):
            for fz in path.iterdir():
                id = self.__objects.add(self.__id, fz.name, fz.is_dir(), parent_id)
                if fz.is_dir():
                    self.dirscan(fz, id)


        def build(self):
            return StorageInfo.build(dict(max_capacity=1000000000, free_space=100000000, volume_identifier=self.__name, storage_description=self.__path))

        def handles(self, parent):
            if parent == 0:
                return self.__objects.keys()
            elif parent == 0xffffffff: # yes, the spec is really dumb
                return self.__objects.handles(0)
            else:
                if not self._objects[parent]._is_dir:
                    raise MTPError("INVALID_PARENT_OBJECT")
                return self.__objects.handles(parent)

        def __getitem__(self, item):
            return self.__objects[item]

    def handles(self, parent):
        return itertools.chain(s.handles(parent) for s in self._props.values())

    def object(self, object):
        for s in self._props.values():
            try:
                return s[object]
            except MTPError:
                continue
        raise MTPError('INVALID_OBJECT_HANDLE')

    def __init__(self, *args):
        super().__init__(self.__Storage, *((n+0x00010001,) + t for (n, t) in enumerate(args)))



if __name__ == '__main__':
    sm = StorageManager(
        ('/tmp/mtp', u'Files', True),
    )

    for k in sm.keys():
        print(k, StorageInfo.parse(sm[k].build()))

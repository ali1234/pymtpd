import itertools

from construct import *

import mtp.constants
from mtp.adapters import MTPString
from mtp.exceptions import MTPError
from mtp.properties import Properties
from mtp.object import ObjectManager


StorageType = Enum(Int16ul, **dict(mtp.constants.storage_types))
StorageFileSystems = Enum(Int16ul, **dict(mtp.constants.storage_file_systems))
StorageAccess = Enum(Int16ul, **dict(mtp.constants.storage_accesss))
AssociationType = Enum(Int16ul, **dict(mtp.constants.association_types))

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
            self.objects = ObjectManager()

        def build(self):
            return StorageInfo.build(dict(max_capacity=1000000000, free_space=100000000, volume_identifier=self.__name, storage_description=self.__path))

        def handles(self, association):
            if association == 0:
                return self.objects.keys()
            else:
                return (k for k, v in self.objects.items() if v._association == association)

    def handles(selfself, association):
        return itertools.chain(s.handles(association) for s in self._props.values())


    def __init__(self, *args):
        super().__init__(self.__Storage, *((n+0x00010001,) + t for (n, t) in enumerate(args)))



if __name__ == '__main__':
    sm = StorageManager(
        ('/tmp/boot', u'boot', True),
        ('/tmp/mnt', u'mnt', False),
        ('/tmp/asdjh', u'Hello', True),
        ('/tmp/asalkdsh', u'Things', True),
    )

    for k in sm.keys():
        print(k, StorageInfo.parse(sm[k].build()))

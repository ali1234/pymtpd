import itertools
import pathlib
import logging
import os
logger = logging.getLogger(__name__)

from construct import *
from inotify_simple import INotify, flags
IN_MASK = flags.ATTRIB | flags.CREATE | flags.DELETE | flags.MODIFY | flags.MOVED_TO | flags.MOVED_FROM | flags.IGNORED

import mtp.constants
from mtp.adapters import MTPString
from mtp.exceptions import MTPError
from mtp.filesystem import FSRootObject


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

    """Basic storage, always empty.."""

    def __init__(self, name, storagemanager):
        self.name = name
        self.sm = storagemanager
        self.sm.register(self)
        logger.debug('Connect %s: %x, %s' % (type(self).__name__, self.storage_id, self.name))

    def disconnect(self):
        logger.debug('Disconnect %s: %x, %s' % (type(self).__name__, self.storage_id, self.name))

    def build(self):
        return StorageInfo.build(dict(max_capacity=self.capacity(), free_space=self.free_space(), volume_identifier=self.name,
                                      storage_description=self.name))

    def capacity(self):
        return 1024*1024*16

    def free_space(self):
        return 1024*1024*5

    def handles(self, parent=0):
        return ()

    def __getitem__(self, item):
        raise MTPError('INVALID_OBJECT_HANDLE')



class FilesystemStorage(Storage):

    def __init__(self, friendlyname, path, storagemanager, handlemanager, watchmanager):
        super().__init__(friendlyname, storagemanager)
        self.hm = handlemanager
        self.wm = watchmanager
        self.root = FSRootObject(path, self)

    def handles(self, recurse = False):
        return self.root.handles(recurse)

    def __getitem__(self, item):
        obj = self.hm[item]
        if obj.storage != self:
            raise MTPError('INVALID_OBJECT_HANDLE')
        else:
            return obj



class StorageManager(object):

    def __init__(self, handlemanager):
        self.counter = itertools.count(0x10001)
        self.stores = dict()
        self.hm = handlemanager
        self.default_store = None

    def register(self, storage):
        storage_id = next(self.counter)
        storage.storage_id = storage_id
        self.stores[storage_id] = storage
        storage.id = storage_id
        if self.default_store == None:
            self.default_store = storage

    def unregister(self, storage):
        del self.stores[storage.storage_id]
        del storage.id
        del storage.storage_id

    def ids(self):
        return self.stores.keys()

    def handles(self, storage, parent):
        if parent == 0: # all objects
            if storage == 0xffffffff: # all storage
                return self.hm.handles()
            else:
                return self.stores[storage].handles(recurse=True)

        elif parent == 0xffffffff: # root objects
            if storage == 0xffffffff:
                return itertools.chain(s.handles(recurse=False) for s in self.stores)
            else:
                return self.stores[storage].handles(recurse=False)

        else: # in dir
            if storage == 0xffffffff:
                return self.hm[parent].handles(recurse=False)
            else:
                return self.stores[storage][parent].handles(recurse=False)

    def __getitem__(self, key):
        try:
            return self.stores[key]
        except KeyError:
            raise MTPError('STORE_NOT_AVAILABLE')



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import asyncio
    loop = asyncio.get_event_loop()
    s = FilesystemStorage('Files', '/tmp/test', writable=True, loop=loop)
    s.connect()
    loop.run_forever()
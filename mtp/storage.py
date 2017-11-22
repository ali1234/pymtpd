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
from mtp.object import Object
from mtp.packets import MTPEvent




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

class BaseStorage(object):

    """Implements basic storage functions: ID, handles, object container."""

    counter = itertools.count(0x10001)

    def __init__(self, name, writable=False):
        self._id = next(self.counter)
        self._name = name
        self._writable = writable
        self._objects = dict()


    def connect(self):
        logger.debug('Connect %s: %x, %s' % ('', self._id, self._name))

    def disconnect(self):
        logger.debug('Disconnect %s: %x, %s' % ('', self._id, self._name))

    def build(self):
        return StorageInfo.build(dict(max_capacity=1000000000, free_space=100000000, volume_identifier=self._name,
                                      storage_description=self._name))

    def handles(self, parent=0):
        if parent == 0:
            return self._objects.keys()
        elif parent == 0xffffffff:  # yes, the spec is really dumb
            return (k for k, v in self._objects.items() if v._parent == None)
        else:
            try:
                p = self._objects[parent]
            except KeyError:
                raise MTPError("INVALID_PARENT_OBJECT")
            else:
                return (k for k, v in self._objects.items() if v._parent == p)

    def __getitem__(self, item):
        try:
            return self._objects[item]
        except KeyError:
            raise MTPError('INVALID_OBJECT_HANDLE')

    def __delitem__(self, item):
        try:
            del self._objects[item]
        except KeyError:
            raise MTPError('INVALID_OBJECT_HANDLE')

class FilesystemStorageInconsistency(Exception):
    """Exception raised if handle<->object mapping is out of sync."""
    pass

class FilesystemStorage(BaseStorage):

    """Implements a storage backed by a filesystem."""

    def __init__(self, name, path, writable=False, eventcb=lambda **kwargs: None, loop=None):
        super().__init__(name, writable)
        self._path = pathlib.Path(path)
        self.__bywd = dict()
        self.__bypath = dict()
        if loop == None:
            loop = asyncio.get_event_loop()
        self.__eventcb = eventcb
        self.__loop = loop

    def connect(self):
        super().connect()
        self.__inotify = INotify()
        self.dirscan(self._path) # objects in root dir have no parent
        self.__loop.add_reader(self.__inotify.fd, self.__inotify_event)

    def dirscan(self, path, parent=None):
        wd = self.__inotify.add_watch(path, IN_MASK)
        self.__bywd[wd] = parent
        for fz in path.iterdir():
            obj = Object(self, fz, parent)
            self._objects[obj._handle] = obj
            self.__bypath[obj._path] = obj
            if fz.is_dir():
                self.dirscan(fz, obj)

    def __inotify_event(self):
        # exceptions here should bubble out to the function and trigger a restart.
        for event in self.__inotify.read():
            parent = self.__bywd[event.wd]
            if parent is None:
                path = event.name
            else:
                path = str(pathlib.Path(parent._path) / event.name)

            if event.mask & (flags.ATTRIB | flags.MODIFY):
                logger.info('MODIFY: %s:%s' % (self._name, path))
                # This one is simple. Just notify that the object changed. Note that gvfs-mtp ignores this anyway.
                handle = self.__bypath[path]._handle
                self.__eventcb(code='OBJECT_INFO_CHANGED', p1=handle)

            elif event.mask & (flags.CREATE):
                logger.info('CREATE: %s:%s' % (self._name, path))
                # This one is simple for files, but if a directory was created then objects may have been
                # created inside it before we received this event, and therefore before we added an inotify
                # watch to the new directory. TODO: handle that case correctly.
                fullpath = self._path / path
                obj = Object(self, fullpath, parent)
                self._objects[obj._handle] = obj
                self.__bypath[path] = obj
                if fullpath.is_dir():
                    self.dirscan(fullpath, obj)
                self.__eventcb(code='OBJECT_ADDED', p1=obj._handle)

            elif event.mask & (flags.DELETE):
                logger.info('DELETE: %s:%s' % (self._name, path))
                # If a directory is deleted it must have already been empty, so nothing fancy is needed here.
                handle = self.__bypath[path]._handle
                del self._objects[handle]
                del self.__bypath[path]
                self.__eventcb(code='OBJECT_REMOVED', p1=handle)

            elif event.mask & (flags.MOVED_FROM):
                # TODO: Implement this
                logger.info('MOVED_FROM: %s:%s' % (self._name, path))

            elif event.mask & (flags.MOVED_TO):
                # TODO: Implement this
                logger.info('MOVED_TO: %s:%s' % (self._name, path))

            elif event.mask & (flags.IGNORED):
                logger.info('IGNORED: %s:%s' % (self._name, path))
                # This event is received when a watched object is deleted.
                # The watch is automatically removed on kernel side.
                if self.__bywd[event.wd] is None:
                    logger.critical('Store root directory appears to have been deleted.')
                del self.__bywd[event.wd]

            else:
                logger.info('BUG: EVENT UNHANDLED: %s:%s %d' % (self._name, path, event.mask))

            logger.info('Event handled successfully?')

    def disconnect(self):
        super().disconnect()
        self.__loop.remove_reader(self.__inotify.fd)
        self.__inotify.close()



class StorageManager(object):

    def __init__(self, eventcb, loop, *stores):
        self.eventcb = eventcb
        self.loop = loop
        self.__stores = dict()
        for s in stores:
            self.add(s)

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

    def add(self, store):
        self.__stores[store._id] = store
        store.connect()
        self.eventcb(code='STORE_ADDED', p1=store._id)

    def __getitem__(self, key):
        try:
            return self.__stores[key]
        except KeyError:
            raise MTPError('STORE_NOT_AVAILABLE')

    def __delitem__(self, key):
        self.__stores[key].disconnect()
        del self.__stores[key]
        self.eventcb(code='STORE_ADDED', p1=key)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import asyncio
    loop = asyncio.get_event_loop()
    s = FilesystemStorage('Files', '/tmp/test', writable=True, loop=loop)
    s.connect()
    loop.run_forever()
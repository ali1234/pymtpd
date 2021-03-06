import pathlib
import shutil
import itertools
import datetime

from inotify_simple import flags

import logging
logger = logging.getLogger(__name__)

from mtp.object import ObjectInfo
from mtp.partialfile import PartialFile
from mtp.exceptions import MTPError


class FSObject(object):

    __slots__ = ('parent', 'storage', 'name', 'handle', 'wd')

    def __init__(self, path, parent, storage):
        self.parent = parent
        self.storage = storage
        self.name = path.name

    def path(self):
        return self.parent.path() / self.name

    def unwatch(self):
        pass

    def unregister_children(self):
        pass

    def create_or_reserve(self, info):
        raise MTPError('INVALID_PARENT_HANDLE')

    def delete(self):
        self.unwatch()
        self.unregister_children()
        if self.path().is_dir():
            shutil.rmtree(str(self.path()))
        else:
            self.path().unlink()
        del self.parent.children[self.name]

    def truncate(self, offset):
        self.path().open('r+b').truncate(offset)

    def partial_file(self, offset, length):
        f = self.path().open('r+b')
        return PartialFile(f, offset, length)

    def handles(self, recurse):
        raise MTPError('INVALID_PARENT_HANDLE')

    def handle_as_parent(self):
        return self.handle

    def build(self):
        path = self.path()
        stat = path.stat()
        is_dir = path.is_dir()
        return ObjectInfo.build(dict(
            storage_id=self.storage.storage_id,
            compressed_size=stat.st_size,
            parent_object=0 if isinstance(self.parent, FSRootObject) else self.parent.handle,
            filename=path.name,
            format='ASSOCIATION' if is_dir else 'UNDEFINED',
            association_type='GENERIC_FOLDER' if is_dir else 'UNDEFINED',
            ctime = datetime.datetime.fromtimestamp(stat.st_ctime),
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime),
        ))

    def open(self, **kwargs):
        return self.path().open(**kwargs)

    def verify(self):
        assert(self.path().exists())
        assert(not self.path().is_dir())



class FSDirObject(FSObject):

    __slots__ = ('children',)

    def __init__(self, path, parent, storage):
        super().__init__(path, parent, storage)
        self.children = {}
        self.storage.wm.register(self)

        for fz in self.path().iterdir():
            self.add_child(fz)

    def add_child(self, path, handle=None):
        if path.is_dir():
            obj = FSDirObject(path, self, self.storage)
        else:
            obj = FSObject(path, self, self.storage)
        self.children[obj.name] = obj
        self.storage.hm.register(obj, handle)
        return obj.handle

    def unwatch(self):
        self.storage.wm.unregister(self)
        for c in self.children:
            c.unwatch()

    def unregister_children(self):
        for c in self.children:
            self.hm.unregister(c)
            c.unregister_children()

    def create_or_reserve(self, info):
        if info.format == 'ASSOCIATION' and info.association_type == 'GENERIC_FOLDER':
            self.path().mkdir(info.name)
            return self.add_child(self.path() / info.filename)
        elif info.compressed_size == 0:
            f = (self.path() / info.filename).open('wb')
            f.close()
            return self.add_child(self.path() / info.filename)
        else:
            return self.storage.hm.reserve_handle()

    def truncate(self, offset):
        raise MTPError('INVALID_OBJECT_HANDLE') # TODO: is this the right error?

    def partial_file(self, offset, length):
        raise MTPError('INVALID_OBJECT_HANDLE')  # TODO: is this the right error?

    def inotify(self, event):
        if event.mask & (flags.ATTRIB | flags.MODIFY):
            logger.debug('MODIFY: %s:%s %s' % (self.storage.name, self.path(), event.name))

        elif event.mask & (flags.CREATE):
            logger.debug('CREATE: %s:%s %s' % (self.storage.name, self.path(), event.name))

        elif event.mask & (flags.CLOSE_WRITE):
            logger.debug('CLOSE_WRITE: %s:%s %s' % (self.storage.name, self.path(), event.name))

        elif event.mask & (flags.DELETE):
            logger.debug('DELETE: %s:%s %s' % (self.storage.name, self.path(), event.name))

        elif event.mask & (flags.MOVED_FROM):
            logger.debug('MOVED_FROM: %s:%s %s' % (self.storage.name, self.path(), event.name))

        elif event.mask & (flags.MOVED_TO):
            logger.debug('MOVED_TO: %s:%s %s' % (self.storage.name, self.path(), event.name))

        else:
            logger.warning('EVENT UNHANDLED: %s:%s %s' % (self.storage.name, self.path(), event.name))

        logger.debug('inotify event handling complete.')

    def handles(self, recurse=False):
        if recurse:
            return itertools.chain(self.handles(False), *(c.handles(True) for c in self.children.values() if isinstance(c, FSDirObject)))
        else:
            return (c.handle for c in self.children.values() if hasattr(c, 'handle'))

    def verify(self):
        logger.debug('Verifying: %s' % (self.path()))
        assert(self.path().exists())
        assert(self.path().is_dir())
        assert(hasattr(self, 'wd'))
        assert(self.storage.wm.watches[self.wd] == self)

        for n,c in self.children.items():
            c.verify()
            assert(c.name == n)
            assert(c.parent == self)
            assert(hasattr(c, 'handle'))
            assert(self.storage.hm.objects[c.handle] == c)

        for p in self.path().iterdir():
            assert(p.name in self.children)


class FSRootObject(FSDirObject):

    __slots__ = ('_path',)

    def __init__(self, path, storage):
        self.storage = storage
        self._path = pathlib.Path(path)
        super().__init__(self._path, None, self.storage)

    def path(self):
        return self._path

    def delete(self):
        logger.error('Cannot delete the storage root.')
        return

    def handle_as_parent(self):
        return 0xffffffff

    def inotify(self, event):
        if event.mask & (flags.ATTRIB | flags.MODIFY) and event.name == '':
            # run a cache verification, triggered by touching the root directory
            logger.warning('Cache verification started')
            self.verify()
            logger.warning('Cache verification finished')
        else:
            super().inotify(event)

    def verify(self):
        super().verify()
        self.storage.hm.verify()
        self.storage.wm.verify()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import asyncio

    from mtp.watchmanager import WatchManager
    from mtp.handlemanager import HandleManager

    loop = asyncio.get_event_loop()

    wm = WatchManager()
    loop.add_reader(wm, wm.dispatch)

    hm = HandleManager()
    r = FSRootObject('Files', pathlib.Path('/tmp/mtp'), None, hm, wm)

    loop.run_forever()
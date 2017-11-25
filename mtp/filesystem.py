import pathlib
import itertools
import datetime

from inotify_simple import flags

import logging
logger = logging.getLogger(__name__)

from mtp.object import ObjectInfo


class FSObject(object):

    def __init__(self, path, parent, storage):
        self.parent = parent
        self.storage = storage
        self.name = path.name

    def path(self):
        return self.parent.path() / self.name

    def unwatch(self):
        pass

    def predelete(self):
        self.unwatch()
        self.storage.hm.predelete(self)

    def handles(self, recurse):
        return ()

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



class FSDirObject(FSObject):

    def __init__(self, path, parent, storage):
        super().__init__(path, parent, storage)
        self.children = {}
        self.storage.wm.register(self)

        for fz in self.path().iterdir():
            self.add_child(fz)

    def add_child(self, path):
        if path.is_dir():
            obj = FSDirObject(path, self, self.storage)
        else:
            obj = FSObject(path, self, self.storage)
        self.children[obj.name] = obj
        self.storage.hm.register(obj)

    def unwatch(self):
        self.storage.wm.unregister(self)
        for c in self.children:
            c.unwatch()

    def inotify(self, event):
        if event.mask & (flags.ATTRIB | flags.MODIFY):
            logger.debug('MODIFY: %s:%s %s' % (self.storage.name, self.path(), event.name))
            # This one is simple. Just notify that the object changed. Note that gvfs-mtp ignores this anyway.
            if event.name == '':
                pass # we might need to handle this later
            else:
                self.storage.hm.eventcb(code='OBJECT_INFO_CHANGED', p1=self.children[event.name].handle)

        elif event.mask & (flags.CREATE):
            logger.debug('CREATE: %s:%s %s' % (self.storage.name, self.path(), event.name))
            # This one is simple for files, but if a directory was created then objects may have been
            # created inside it before we received this event, and therefore before we added an inotify
            # watch to the new directory. TODO: handle that case correctly.

        elif event.mask & (flags.DELETE):
            logger.debug('DELETE: %s:%s %s' % (self.storage.name, self.path(), event.name))
            # If a directory is deleted it must have already been empty, so nothing fancy is needed here.
            obj = self.children[event.name]
            self.storage.hm.unregister(obj)
            del self.children[event.name]

        elif event.mask & (flags.MOVED_FROM):
            logger.debug('MOVED_FROM: %s:%s %s' % (self.storage.name, self.path(), event.name))
            # TODO: Implement this

        elif event.mask & (flags.MOVED_TO):
            logger.debug('MOVED_TO: %s:%s %s' % (self.storage.name, self.path(), event.name))
            # TODO: Implement this

        else:
            logger.warning('EVENT UNHANDLED: %s:%s %s' % (self.storage.name, self.path(), event.name))

        logger.debug('inotify event handling complete.')

    def handles(self, recurse=False):
        if recurse:
            return itertools.chain(self.handles(False), *(c.handles(True) for c in self.children.values()))
        else:
            return (c.handle for c in self.children.values() if hasattr(c, 'handle'))



class FSRootObject(FSDirObject):

    def __init__(self, path, storage):
        self.storage = storage
        self._path = pathlib.Path(path)
        super().__init__(self._path, None, self.storage)

    def path(self):
        return self._path



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
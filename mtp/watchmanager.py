from inotify_simple import INotify, flags
IN_MASK = flags.ATTRIB | flags.CREATE | flags.DELETE | flags.MODIFY | flags.MOVED_TO | flags.MOVED_FROM | flags.IGNORED | flags.CLOSE_WRITE

import logging
logger = logging.getLogger(__name__)


class WatchManager(object):

    def __init__(self):
        self.inotify = INotify()
        self.watches = {}

    def register(self, obj):
        wd = self.inotify.add_watch(obj.path(), IN_MASK)
        obj.wd = wd
        self.watches[wd] = obj

    def unregister(self, obj):
        logger.debug('Unwatching %s.' % (obj.path()))
        try:
            del self.watches[obj.wd]
            self.inotify.rm_watch(obj.wd)
        except AttributeError:
            logger.error('Object %s has no watch descriptor.' % (obj.path()))
        except KeyError:
            logger.error('Object %s has a watch descriptor but is not known to watch manager.' % (obj.path()))

    def fileno(self):
        return self.inotify.fd

    def dispatch(self):
        for event in self.inotify.read(read_delay=1000):
            if event.mask & flags.IGNORED:
                if event.wd in self.watches:
                    del self.watches[event.wd].wd
                    del self.watches[event.wd]
                else:
                    logger.warning('Received ignore event for object we were not watching: %s %s.' % (event.path, event.name))
            else:
                if event.wd in self.watches:
                    self.watches[event.wd].inotify(event)
                else:
                    logger.warning('Received event for object we were not watching: %s %s.' % (event.path, event.name))

    def verify(self):
        for obj in self.watches.values():
            assert(obj.path().exists())
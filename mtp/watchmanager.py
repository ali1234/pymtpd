from inotify_simple import INotify, flags
IN_MASK = flags.ATTRIB | flags.CREATE | flags.DELETE | flags.MODIFY | flags.MOVED_TO | flags.MOVED_FROM | flags.IGNORED

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
        logger.debug('unregister %s' % (str(obj.path())))
        self.inotify.rm_watch(obj.wd)
        del self.watches[obj.wd]
        del obj.wd

    def fileno(self):
        return self.inotify.fd

    def dispatch(self):
        for event in self.inotify.read():
            if event.mask & flags.IGNORED:
                if event.wd in self.watches:
                    del self.watches[event.wd].wd
                    del self.watches[event.wd]
            else:
                self.watches[event.wd].inotify(event)
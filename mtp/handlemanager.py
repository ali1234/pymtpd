import itertools

import logging
logger = logging.getLogger(__name__)

from mtp.exceptions import MTPError


class HandleManager(object):

    def __init__(self, eventcb):
        self.counter = itertools.count(1)
        self.objects = {}
        self._predelete = {}
        self.eventcb = eventcb

    def register(self, obj):
        handle = next(self.counter)
        obj.handle = handle
        self.objects[handle] = obj
        self.eventcb(code='OBJECT_ADDED', p1=obj.handle) # TODO: don't do this if the object is in precreate.
        return handle

    def unregister(self, obj):
        if obj.handle in self._predelete:
            del self._predelete[obj.handle]
        elif obj.handle in self.objects:
            del self.objects[obj.handle]
            self.eventcb(code='OBJECT_REMOVED', p1=obj.handle)
        else:
            logger.error('Object has handle but is not registered')
        del obj.handle

    def predelete(self, obj):
        logger.debug('Preparing %s for deletion.' % (obj.path()))
        try:
            del self.objects[obj.handle]
        except AttributeError:
            logger.error('Object %s has no handle.' % (obj.path()))
        except KeyError:
            logger.error('Object %s has a handle but is not known to handle manager.' % (obj.path()))
        else:
            self._predelete[obj.handle] = obj

    def handles(self):
        return self.objects.keys()

    def __getitem__(self, handle):
        try:
            return self.objects[handle]
        except KeyError:
            raise MTPError('INVALID_OBJECT_HANDLE')
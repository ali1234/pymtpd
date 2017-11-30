import itertools

import logging
logger = logging.getLogger(__name__)

from mtp.exceptions import MTPError


class HandleManager(object):

    def __init__(self, eventcb):
        self.counter = itertools.count(1)
        self.objects = {}
        self.eventcb = eventcb

    def register(self, obj, send_event=True, handle=None):
        if handle is None:
            handle = next(self.counter)
        elif handle in self.objects:
            logger.error('Trying to register an object to an already used handle.')
        if hasattr(obj, 'handle'):
            if obj.handle in self.objects:
                logger.error('Object is already registered.')
            else:
                logger.error('Object already has a handle but it is not known to this handle manager.')
        obj.handle = handle
        self.objects[handle] = obj
        if send_event:
            self.eventcb(code='OBJECT_ADDED', p1=obj.handle)
        return handle

    def unregister(self, obj, send_event=True):
        try:
            handle = obj.handle
            del self.objects[handle]
        except AttributeError:
            logger.error('Object %s has no handle.' % (obj.path()))
        except KeyError:
            logger.error('Object %s has a handle but is not known to handle manager.' % (obj.path()))
        else:
            del obj.handle
            if send_event:
                self.eventcb(code='OBJECT_REMOVED', p1=handle)

    def reserve_handle(self):
        return next(self.counter)

    def handles(self):
        return self.objects.keys()

    def __getitem__(self, handle):
        try:
            return self.objects[handle]
        except KeyError:
            raise MTPError('INVALID_OBJECT_HANDLE')

    def verify(self):
        for obj in self.objects.values():
            assert(obj.path().exists())
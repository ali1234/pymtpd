import itertools

from mtp.exceptions import MTPError


class HandleManager(object):

    def __init__(self):
        self.counter = itertools.count(1)
        self.objects = {}

    def register(self, obj):
        handle = next(self.counter)
        obj.handle = handle
        self.objects[handle] = obj
        return handle

    def unregister(self, obj):
        del self.objects[obj.handle]
        del obj.handle

    def handles(self):
        return self.objects.keys()

    def __getitem__(self, handle):
        try:
            return self.objects[handle]
        except KeyError:
            raise MTPError(code='INVALID_OBJECT_HANDLE')
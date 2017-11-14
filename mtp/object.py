import itertools
from construct import *

import mtp.constants
from mtp.properties import Properties

FormatType = Enum(Int16ul, **dict(mtp.constants.format_types))
ObjectPropertyCode = Enum(Int16ul, **dict(mtp.constants.object_property_codes))


class ObjectManager(Properties):

    counter = itertools.count(1) # start object IDs from 1

    class __Object(object):

        def __init__(self, handle, association):
            self._handle = handle
            self._association = association

        #def build(self):
        #    return ObjectInfo.build(dict(max_capacity=1000000000, free_space=100000000, volume_identifier=self.__name, storage_description=self.__path))

    def __init__(self, *args):
        super().__init__(self.__Object, *((next(self.counter),) + t for t in args))

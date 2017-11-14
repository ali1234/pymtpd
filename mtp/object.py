import itertools
from construct import *

import mtp.constants
from mtp.exceptions import MTPError
from mtp.properties import Properties
from mtp.adapters import MTPString, MTPDateTime

FormatType = Enum(Int16ul, **dict(mtp.constants.format_types))
ObjectPropertyCode = Enum(Int16ul, **dict(mtp.constants.object_property_codes))
AssociationType = Enum(Int16ul, **dict(mtp.constants.association_types))


ObjectInfo = Struct(
    'storage_id' / Int32ul,
    'format' / FormatType,
    'protection' / Int16ul,
    'thumb_format' / FormatType,
    'thumb_compressed_size' / Int32ul,
    'thumb_width' / Int32ul,
    'thumb_height' / Int32ul,
    'image_width' / Int32ul,
    'image_height' / Int32ul,
    'image_bit_depth' / Int32ul,
    'parent_object' / Int32ul,
    'association_type' / AssociationType,
    'association_description' / Int32ul, # what is this?
    'sequence_number' / Int32ul,
    'filename' / MTPString,
    'ctime' / MTPString,
    'mtime' / MTPString,
    'keywords' / MTPString,
)

class ObjectManager(Properties):

    counter = itertools.count(1) # start object IDs from 1

    class __Object(object):

        key_error = MTPError('INVALID_OBJECT_HANDLE')

        def __init__(self, handle, association):
            self._handle = handle
            self._association = association

        #def build(self):
        #    return ObjectInfo.build(dict(max_capacity=1000000000, free_space=100000000, volume_identifier=self.__name, storage_description=self.__path))

    def __init__(self, *args):
        super().__init__(self.__Object, *((next(self.counter),) + t for t in args))

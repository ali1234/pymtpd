import itertools, datetime
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
    'format' / Default(FormatType, 'UNDEFINED'),
    'protection' / Default(Int16ul, 0),
    'compressed_size' / Default(Int32ul, 0),
    'thumb_format' / Default(FormatType, 'UNDEFINED'),
    'thumb_compressed_size' / Default(Int32ul, 0),
    'thumb_width' / Default(Int32ul, 0),
    'thumb_height' / Default(Int32ul, 0),
    'image_width' / Default(Int32ul, 0),
    'image_height' / Default(Int32ul, 0),
    'image_bit_depth' / Default(Int32ul, 0),
    'parent_object' / Int32ul,
    'association_type' / AssociationType,
    'association_description' / Default(Int32ul, 0), # what is this?
    'sequence_number' / Default(Int32ul, 0),
    'filename' / MTPString,
    'ctime' / Default(MTPDateTime, datetime.datetime.now()),
    'mtime' / Default(MTPDateTime, datetime.datetime.now()),
    'keywords' / Default(MTPString, u''),
)

class ObjectManager(Properties):

    counter = itertools.count(1) # start object IDs from 1

    class __Object(object):

        key_error = MTPError('INVALID_OBJECT_HANDLE')

        def __init__(self, storage_id, handle, filename, is_dir, parent):
            self._storage_id = storage_id
            self._handle = handle
            self._filename = filename
            self._is_dir = is_dir
            self._parent = parent
            print(self._handle, self._filename, self._is_dir, self._parent)


        def build(self):
            return ObjectInfo.build(dict(
                storage_id = self._storage_id,
                parent_object = self._parent,
                filename = self._filename,
                association_type = 'GENERIC_FOLDER' if self._is_dir else 'UNDEFINED'
            ))

    def __init__(self, *args):
        super().__init__(self.__Object, *((next(self.counter),) + t for t in args))

    def add(self, *args):
        id = next(self.counter)
        self._props[id] = self._proptype(id, *args)
        return id
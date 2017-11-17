import itertools, datetime

import logging
logger = logging.getLogger(__name__)

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

        keyerror = MTPError('INVALID_OBJECT_HANDLE')

        def __init__(self, handle, storage, filename, is_dir, parent):
            self._storage = storage
            self._handle = handle
            self._filename = filename
            self._is_dir = is_dir
            self._parent = parent
            logger.debug(self.reconstruct_path())

        def raw(self):
            if self._is_dir:
                raise MTPError("INVALID_OBJECT_HANDLE")
            return b'***FILE CONTENTS GOES HERE***'

        def build(self):
            return ObjectInfo.build(dict(
                storage_id = self._storage._id,
                parent_object = 0 if self._parent is None else self._parent._handle,
                filename = self._filename,
                format = 'ASSOCIATION' if self._is_dir else 'UNDEFINED',
                association_type = 'GENERIC_FOLDER' if self._is_dir else 'UNDEFINED'
            ))

        def reconstruct_path(self):
            if self._parent == None:
                return self._storage._path / self._filename
            else:
                return self._parent.reconstruct_path() / self._filename

    def __init__(self):
        super().__init__(self.__Object)

    def handles(self, parent):
        return (k for k, v in self._props.items() if v._parent == parent)

    def add(self, *args):
        id = next(self.counter)
        obj = self._proptype(id, *args)
        self._props[id] = obj
        return obj
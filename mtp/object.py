import itertools, datetime

import logging
logger = logging.getLogger(__name__)

from construct import *

import mtp.constants
from mtp.exceptions import MTPError
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


class Object(object):

    counter = itertools.count(1) # start object IDs from 1

    def __init__(self, storage, path, parent):
        self._storage = storage
        self._handle = next(self.counter)
        self._path = path
        self._parent = parent
        logger.debug(self._path)

    def build(self):
        stat = self._path.stat()
        is_dir = self._path.is_dir()
        return ObjectInfo.build(dict(
            storage_id=self._storage._id,
            compressed_size=self._path.stat().st_size,
            parent_object=0 if self._parent is None else self._parent._handle,
            filename=self._path.name,
            format='ASSOCIATION' if is_dir else 'UNDEFINED',
            association_type='GENERIC_FOLDER' if is_dir else 'UNDEFINED',
            ctime = datetime.datetime.fromtimestamp(stat.st_ctime),
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime),
        ))

    def open(self, *args):
        return self._path.open(*args)


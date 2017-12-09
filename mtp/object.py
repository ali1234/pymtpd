import itertools, datetime

import logging
logger = logging.getLogger(__name__)

from construct import *

import mtp.constants
from mtp.exceptions import MTPError
from mtp.adapters import MTPString, MTPDateTime
from mtp.packets import DataType

FormatType = Enum(Int16ul, **dict(mtp.constants.format_types))

ObjectPropertyCode = Enum(Int16ul, **{x[0]: x[1] for x in mtp.constants.object_property_codes})
ObjectPropertyCode.consttypes = {x[0]: Const(DataType, x[2]) for x in mtp.constants.object_property_codes}
ObjectPropertyCode.formats = {x[0]: DataType.formats[x[2]] for x in mtp.constants.object_property_codes}

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

ObjectPropertyCodeArray = PrefixedArray(Int32ul, ObjectPropertyCode)

ObjectPropertyDesc = Struct(
    'code' / ObjectPropertyCode,
    'type' / Switch(this.code, ObjectPropertyCode.consttypes),
    'writable' / Default(Byte, True),
    'default' / Switch(this.code, ObjectPropertyCode.formats),
    'group' / Const(Int32ul, 0),
    'form' / Const(Byte, 0),
)

def builddesc(prop):
    if ObjectPropertyCode.formats[prop] == MTPString:
        return ObjectPropertyDesc.build(dict(code=prop, default=''))
    else:
        return ObjectPropertyDesc.build(dict(code=prop, default=0))
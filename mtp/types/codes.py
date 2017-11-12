from construct import *

from . import constants


def l2d(l, a=0, b=1, wrap=lambda x: x):
    return {x[a]: wrap(x[b]) for x in l}

def EnumList(format, l, a=0, b=1):
    return Enum(format, **l2d(l, a, b))

ContainerType = EnumList(Int16ul, constants.container_types)

DataType = EnumList(Int16ul, constants.data_types)
DataType.formats = l2d(constants.data_types, 0, 2)

FormatType = EnumList(Int16ul, constants.format_types)

ObjectPropertyCode = EnumList(Int16ul, constants.object_property_codes)

DevicePropertyCode = EnumList(Int16ul, constants.device_property_codes)
DevicePropertyCode.consttypes = l2d(constants.device_property_codes, 0, 2, lambda x: Const(DataType, x))
DevicePropertyCode.formats = l2d(constants.device_property_codes, 0, 2, lambda x: DataType.formats[x])

OperationCode = EnumList(Int16ul, constants.operation_codes)

ResponseCode = EnumList(Int16ul, constants.response_codes)

EventCode = EnumList(Int16ul, constants.event_codes)

StorageType = EnumList(Int16ul, constants.storage_types)

StorageAccess = EnumList(Int16ul, constants.storage_accesss)

AssociationType = EnumList(Int16ul, constants.association_types)










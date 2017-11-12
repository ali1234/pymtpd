from construct import *

from mtp.mtpstring import MTPString
import mtp.constants as constants

class MTPError(Exception):
    def __init__(self, code, params=()):
        super().__init__(code)
        self.code = code
        self.params = params

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


MTPDeviceInfo = Struct(
    'standard_version' / Const(Int16ul, constants.VERSION),
    'vendor_extension_id' / Const(Int32ul, 0xffffffff),
    'version' / Default(Int16ul, 0),
    'extensions' / Default(MTPString, ''),
    'functional_mode' / Default(Int16ul, 0),
    'operations_supported' / Default(PrefixedArray(Int32ul, OperationCode), []),
    'events_supported' / Default(PrefixedArray(Int32ul, EventCode), []),
    'device_properties_supported' / Default(PrefixedArray(Int32ul, DevicePropertyCode), []),
    'capture_formats' / Default(PrefixedArray(Int32ul, FormatType), []),
    'playback_formats' / Default(PrefixedArray(Int32ul, FormatType), []),
    'manufacturer' / Default(MTPString, 'Foo Inc.'),
    'model' / Default(MTPString, 'Whizzotron'),
    'device_version' / Default(MTPString, '1.0.0'),
    'serial_number' / Default(MTPString, '123987564'),
)







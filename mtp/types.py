from construct import *
from construct.lib import *

from mtp.propertymanager import PropertyManager
from .mtpstring import MTPString
from .constants import *

class MTPError(Exception):
    def __init__(self, code, params=()):
        super().__init__(code)
        self.code = code
        self.params = params

def l2d(l, a=0, b=1, wrap=lambda x: x):
    return {x[a]: wrap(x[b]) for x in l}

def EnumList(format, l, a=0, b=1):
    return Enum(format, **l2d(l, a, b))

ContainerType = EnumList(Int16ul, container_types)

DataType = EnumList(Int16ul, data_types)
DataType.formats = l2d(data_types, 0, 2)

FormatType = EnumList(Int16ul, format_types)

ObjectPropertyCode = EnumList(Int16ul, object_property_codes)

DevicePropertyCode = EnumList(Int16ul, device_property_codes)
DevicePropertyCode.consttypes = l2d(device_property_codes, 0, 2, lambda x: Const(DataType, x))
DevicePropertyCode.formats = l2d(device_property_codes, 0, 2, lambda x: DataType.formats[x])

OperationCode = EnumList(Int16ul, operation_codes)

ResponseCode = EnumList(Int16ul, response_codes)

EventCode = EnumList(Int16ul, event_codes)

StorageType = EnumList(Int16ul, storage_types)

StorageAccess = EnumList(Int16ul, storage_accesss)

AssociationType = EnumList(Int16ul, association_types)


MTPDeviceInfo = Struct(
    'standard_version' / Const(Int16ul, VERSION),
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







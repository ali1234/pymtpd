from construct import *
from construct.lib import *

from .constants import *
from .types import *




mtp_device_info = Struct(
    'standard_version' / Const(Int16ul, VERSION),
    'vendor_extension_id' / Const(Int32ul, 0xffffffff),
    'version' / Default(Int16ul, 0),
    'extensions' / Default(MTPString(), 'Hello'),
    'functional_mode' / Default(Int16ul, 0),
    'operations_supported' / Default(PrefixedArray(Int32ul, operation_code), []),
    'events_supported' / Default(PrefixedArray(Int32ul, event_code), []),
    'device_properties_supported' / Default(PrefixedArray(Int32ul, device_property_code), []),
    'capture_formats' / Default(PrefixedArray(Int32ul, format_type), []),
    'playback_formats' / Default(PrefixedArray(Int32ul, format_type), []),
    'manufacturer' / Default(MTPString(), 'Foo Inc.'),
    'model' / Default(MTPString(), 'Whizzotron'),
    'device_version' / Default(MTPString(), '1.0.0'),
    'serial_number' / Default(MTPString(), '123987564'),
)


if __name__ == '__main__':
    from binascii import hexlify

    b = mtp_device_info.build(dict(operations_supported=['GET_DEVICE_INFO']))
    p = mtp_device_info.parse(b)
    print(p)
    print(hexlify(b))

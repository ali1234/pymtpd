from construct import *
from construct.lib import *

from .types import MTPString
from .constants import *


mtp_device_info = Struct(
    'standard_version' / Const(Int16ul, VERSION),
    'vendor_extension_id' / Const(Int32ul, 0xffffffff),
    'version' / Default(Int16ul, 0),
    'extensions' / Default(MTPString, ''),
    'functional_mode' / Default(Int16ul, 0),
    'operations_supported' / Default(PrefixedArray(Int32ul, operation_code), []),
    'events_supported' / Default(PrefixedArray(Int32ul, event_code), []),
    'device_properties_supported' / Default(PrefixedArray(Int32ul, device_property_code), []),
    'capture_formats' / Default(PrefixedArray(Int32ul, format_type), []),
    'playback_formats' / Default(PrefixedArray(Int32ul, format_type), []),
    'manufacturer' / Default(MTPString, 'Foo Inc.'),
    'model' / Default(MTPString, 'Whizzotron'),
    'device_version' / Default(MTPString, '1.0.0'),
    'serial_number' / Default(MTPString, '123987564'),
)

device_property_type = {
    'DEVICE_FRIENDLY_NAME': Const(format_type, 'STR'),
    'SYNCHRONIZATION_PARTNER': Const(format_type, 'STR'),
}

device_property_cons = {
    'STR': MTPString,
}

device_property_desc = Struct(
    'code' / device_property_code,
    'type' / Switch(this.code, device_property_type),
    'writable' / Default(Byte, False),
    'default' / Switch(this.type, device_property_cons),
    'current' / Switch(this.type, device_property_cons),
    'form' / Const(Byte, 0),
)

if __name__ == '__main__':

    print(MTPString.build(''))
    print(MTPString.build('A'))
    print(MTPString.build('hello'))

    print(MTPString.parse(b'\x00'))
    print(MTPString.parse(b'\x02A\x00\x00\x00'))
    print(MTPString.parse(b'\x06h\x00e\x00l\x00l\x00o\x00\x00\x00'))

    import code
    code.interact(local=locals())

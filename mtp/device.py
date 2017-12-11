from construct import *

from mtp import constants
from mtp.exceptions import MTPError
from mtp.packets import EventCode, OperationCode, DataType, DataFormats
from mtp.object import FormatType
from mtp.adapters import MTPString


DevicePropertyCode = Enum(Int16ul, **{x[0]: x[1] for x in constants.device_property_codes})
DevicePropertyTypes = {x[0]: Const(DataType, x[2]) for x in constants.device_property_codes}
DevicePropertyFormats = {x[0]: DataFormats[x[2]] for x in constants.device_property_codes}

DeviceInfo = Struct(
    'standard_version' / Const(Int16ul, constants.VERSION),
    'vendor_extension_id' / Const(Int32ul, 0x00000006),
    'version' / Default(Int16ul, 0),
    'extensions' / Default(MTPString, 'microsoft.com: 1.0; android.com: 1.0;'),
    'functional_mode' / Default(Int16ul, 0),
    'operations_supported' / Default(PrefixedArray(Int32ul, OperationCode), []),
    'events_supported' / Default(PrefixedArray(Int32ul, EventCode), []),
    'device_properties_supported' / Default(PrefixedArray(Int32ul, DevicePropertyCode), []),
    'capture_formats' / Default(PrefixedArray(Int32ul, FormatType), ['UNDEFINED', 'ASSOCIATION']),
    'playback_formats' / Default(PrefixedArray(Int32ul, FormatType), ['UNDEFINED', 'ASSOCIATION']),
    'manufacturer' / Default(MTPString, 'Foo Inc.'),
    'model' / Default(MTPString, 'Whizzotron'),
    'device_version' / Default(MTPString, '1.0.0'),
    'serial_number' / Default(MTPString, '123987564'),
)

DevicePropertyDesc = Struct(
    'code' / DevicePropertyCode,
    'type' / Switch(this.code, DevicePropertyTypes),
    'writable' / Default(Byte, False),
    'default' / Switch(this.code, DevicePropertyFormats),
    'current' / Switch(this.code, DevicePropertyFormats),
    'form' / Const(Byte, 0),
)


class DeviceProperty(object):

    def __init__(self, code, default, writable=False):
        self.__code = code
        self.__default = default
        self.__current = default
        self.__writable = writable

    def set(self, value):
        self.__current = value

    def reset(self, force=False):
        if not force and not self.__writable:
            raise MTPError('ACCESS_DENIED')
        self.__current = self.__default

    def parse(self, value):
        if not self.__writable:
            raise MTPError('ACCESS_DENIED')
        self.__current = DevicePropertyFormats[self.__code].parse(value)

    def build(self):
        return DevicePropertyFormats[self.__code].build(self.__current)

    def builddesc(self):
        return DevicePropertyDesc.build(dict(
            code=self.__code,
            writable=self.__writable,
            default=self.__default,
            current=self.__current,
        ))


class DeviceProperties(object):

    def __init__(self, *args):
        self.__props = dict()
        for arg in args:
            self.__props[arg[0]] = DeviceProperty(*arg)

    def supported(self):
        return sorted(self.__props.keys(), key=lambda p: DevicePropertyCode.encmapping[p])

    def reset(self):
        for p in self.__props:
            p.reset(force=True)

    def __getitem__(self, key):
        try:
            return self.__props[key]
        except KeyError:
            raise MTPError('DEVICE_PROP_NOT_SUPPORTED')


if __name__ == '__main__':
    p = DeviceProperties(
        ('DEVICE_FRIENDLY_NAME', 'Some Name', True),
    )

    print(p['DEVICE_FRIENDLY_NAME'].build())
    print(p['DEVICE_FRIENDLY_NAME'].builddesc())
    
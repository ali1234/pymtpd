from construct import *

from mtp import constants
from mtp.exceptions import MTPError
from mtp.properties import Properties
from mtp.packets import EventCode, OperationCode, DataType
from mtp.object import FormatType
from mtp.adapters import MTPString


DevicePropertyCode = Enum(Int16ul, **{x[0]: x[1] for x in constants.device_property_codes})
DevicePropertyCode.consttypes = {x[0]: Const(DataType, x[2]) for x in constants.device_property_codes}
DevicePropertyCode.formats = {x[0]: DataType.formats[x[2]] for x in constants.device_property_codes}

DeviceInfo = Struct(
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

DevicePropertyDesc = Struct(
    'code' / DevicePropertyCode,
    'type' / Switch(this.code, DevicePropertyCode.consttypes),
    'writable' / Default(Byte, False),
    'default' / Switch(this.code, DevicePropertyCode.formats),
    'current' / Switch(this.code, DevicePropertyCode.formats),
    'form' / Const(Byte, 0),
)

class DeviceProperties(Properties):
    class __DeviceProperty(object):
        keyerror = MTPError('DEVICE_PROP_NOT_SUPPORTED')

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
            self.__current = DevicePropertyCode.formats[self.__code].parse(value)

        def build(self):
            return DevicePropertyCode.formats[self.__code].build(self.__current)

        def builddesc(self):
            return DevicePropertyDesc.build(dict(
                code=self.__code,
                writable=self.__writable,
                default=self.__default,
                current=self.__current,
            ))

    def __init__(self, *args):
        super().__init__(self.__DeviceProperty, *args)

    def reset(self):
        for p in self._props:
            p.reset(force=True)


if __name__ == '__main__':
    p = DeviceProperties(
        ('DEVICE_FRIENDLY_NAME', 'Some Name', True),
    )

    print(p['DEVICE_FRIENDLY_NAME'].build())
    print(p['DEVICE_FRIENDLY_NAME'].builddesc())
    
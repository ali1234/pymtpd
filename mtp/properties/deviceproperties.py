from construct import Struct, Switch, Default, Const, Byte, this

from mtp.properties.propertymanager import PropertyManager
from mtp.types import MTPError, DevicePropertyCode

DevicePropertyDesc = Struct(
    'code' / DevicePropertyCode,
    'type' / Switch(this.code, DevicePropertyCode.consttypes),
    'writable' / Default(Byte, False),
    'default' / Switch(this.code, DevicePropertyCode.formats),
    'current' / Switch(this.code, DevicePropertyCode.formats),
    'form' / Const(Byte, 0),
)

class DeviceProperty(object):
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


class DeviceProperties(PropertyManager):
    def __init__(self, *args):
        super().__init__(DeviceProperty, *args)

    def reset(self):
        for p in self._props:
            p.reset(force=True)
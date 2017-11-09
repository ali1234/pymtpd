import ctypes

u8 = ctypes.c_ubyte
assert ctypes.sizeof(u8) == 1
le16 = ctypes.c_ushort
assert ctypes.sizeof(le16) == 2
le32 = ctypes.c_uint
assert ctypes.sizeof(le32) == 4

from . import constants

class MTPHeader(ctypes.LittleEndianStructure):

    def __init__(self, **kwargs):
        self.type = self._type_
        self.code = self._code_
        super(MTPHeader, self).__init__(**kwargs)

    _type_ = constants.MTP_CONTAINER_TYPE_UNDEFINED
    _code_ = 0

    _pack_ = 1
    _fields_ = [
        ('length', le32),
        ('type', le16),
        ('code', le16),
        ('transaction_id', le32),
    ]



class MTPResponse(MTPHeader):
    _type_ = constants.MTP_CONTAINER_TYPE_RESPONSE



class MTPData(MTPHeader):
    _type_ = constants.MTP_CONTAINER_TYPE_DATA
    _pack_ = 1
    _fields_ = [
        ('data', u8*500),
    ]


class MTPOperation(MTPHeader):
    _type_ = constants.MTP_CONTAINER_TYPE_COMMAND


class MTPOperationOpenSession(MTPOperation):
    _code_ = constants.MTP_OPERATION_OPEN_SESSION
    _fields_ = [
        ('session_id', le32),
    ]


class MTPOperationGetDeviceInfo(MTPOperation):
    _code_ = constants.MTP_OPERATION_GET_DEVICE_INFO




parse_map = {}
for klass in MTPHeader.__subclasses__():
    parse_map[klass._type_] = {
        innerklass._code_: innerklass for innerklass in klass.__subclasses__()
    }

def parse(buffer):
    h = MTPHeader.from_buffer(buffer)
    try:
        return parse_map[h.type][h.code].from_buffer(buffer)
    except KeyError as e:
        print('Unknown packet received:', h.length, h.type, hex(h.code))
        raise e

if __name__ == '__main__':
    p = MTPCommandOpenSession(length=1, type=2, code=3, transaction_id=4, session_id=5)
    print(buffer(p))
